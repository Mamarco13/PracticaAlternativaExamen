import pandas as pd
import os
import sys

# Detectar modo desde argumentos
mode = "--std"
for arg in sys.argv:
    if arg in ("--bl", "--blplus"):
        mode = arg

if mode == "--bl":
    alg_name = "HHO_BL"
elif mode == "--blplus":
    alg_name = "HHO_BLplus"
else:
    alg_name = "HHO"

# Configuración
RESULT_DIR = "results_cec_batch"
DIM = 30

# Milestones usados por TacoLab
milestones = [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
NUM_RUNS = len(milestones)

# Asegurar columnas F01–F30
summary = {}
for i in range(1, 31):
    col = f"F{i:02d}"
    suffix = alg_name.replace("HHO_", "HHOBL") if "BL" in alg_name else alg_name
    csv_path = os.path.join(RESULT_DIR, f"F{i}_results_{suffix}.csv")
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
        values = data["Fitness"].dropna().values
        summary[col] = list(values[:NUM_RUNS]) + [1e10] * (NUM_RUNS - len(values))
    else:
        summary[col] = [1e10] * NUM_RUNS

# Metadatos Tacolab
summary["milestone"] = milestones
summary["dimension"] = [DIM] * NUM_RUNS
summary["alg"] = [alg_name] * NUM_RUNS

# Orden Tacolab
ordered_cols = ["milestone"] + [f"F{i:02d}" for i in range(1, 31)] + ["dimension", "alg"]
df = pd.DataFrame(summary)[ordered_cols]

# Exportar a XLSX
xlsx_path = os.path.join(RESULT_DIR, f"cec2017_{alg_name}_D{DIM}.xlsx")
df.to_excel(xlsx_path, index=False, engine="openpyxl")

print(f"Excel TACOLAB con milestones correcto generado: {xlsx_path}")
