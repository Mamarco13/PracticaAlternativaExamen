import pandas as pd
import os

# Configuración
RESULT_DIR = "results_cec_batch"
DIM = 30
NUM_RUNS = 51

# Milestones correctos según formato oficial
milestones = [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
NUM_RUNS = len(milestones)

# Asegurar columnas F01–F30
summary = {}
for i in range(1, 31):
    col = f"F{i:02d}"
    csv_path = os.path.join(RESULT_DIR, f"F{i}_results.csv")
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
        values = data["Fitness"].dropna().values
        summary[col] = list(values[:NUM_RUNS]) + [1e10] * (NUM_RUNS - len(values))
    else:
        summary[col] = [1e10] * NUM_RUNS

# Metadatos Tacolab
summary["milestone"] = milestones
summary["dimension"] = [DIM] * NUM_RUNS
summary["alg"] = ["HHO"] * NUM_RUNS

# Orden Tacolab
ordered_cols = ["milestone"] + [f"F{i:02d}" for i in range(1, 31)] + ["dimension", "alg"]
df = pd.DataFrame(summary)[ordered_cols]

# Exportar a XLSX
xlsx_path = os.path.join(RESULT_DIR, f"cec2017_HHO_D{DIM}.xlsx")
df.to_excel(xlsx_path, index=False, engine="openpyxl")

print(f"Excel TACOLAB con milestones correctos generado: {xlsx_path}")
