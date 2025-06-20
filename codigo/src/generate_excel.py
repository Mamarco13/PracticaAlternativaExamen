import pandas as pd
import os

# Configuración
RESULT_DIR = "results_cec_batch"
ALGORITHMS = {
    "HHO": "HHO",
    "HHOBL": "HHO_BL",
    "HHOBLplus": "HHO_BLplus"
}
DIM = 30
NUM_FUNCTIONS = 30
MILESTONES = [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
NUM_RUNS = len(MILESTONES)

# Crear estructura para guardar todas las ejecuciones por algoritmo
combined_rows = []

# Iterar sobre algoritmos
for file_suffix, alg_name in ALGORITHMS.items():
    print(f"Procesando {alg_name}...")
    function_results = {f"F{i:02d}": [] for i in range(1, NUM_FUNCTIONS + 1)}

    for i in range(1, NUM_FUNCTIONS + 1):
        col = f"F{i:02d}"
        csv_path = os.path.join(RESULT_DIR, f"F{i}_results_{file_suffix}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            fitness_vals = df["Fitness"].dropna().values
            if len(fitness_vals) < NUM_RUNS:
                fitness_vals = list(fitness_vals) + [1e10] * (NUM_RUNS - len(fitness_vals))
            function_results[col] = fitness_vals[:NUM_RUNS]
        else:
            function_results[col] = [1e10] * NUM_RUNS
            print(f"Archivo faltante: {csv_path} → valores 1e10 insertados")

    # Transponer resultados por ejecución
    for idx, milestone in enumerate(MILESTONES):
        row = {f"F{i:02d}": function_results[f"F{i:02d}"][idx] for i in range(1, NUM_FUNCTIONS + 1)}
        row["milestone"] = milestone
        row["alg"] = alg_name
        combined_rows.append(row)

# Crear DataFrame final
df_all = pd.DataFrame(combined_rows)

# Guardar Excel
output_path = os.path.join(RESULT_DIR, "cec2017_ALL_algorithms.xlsx")
df_all.to_excel(output_path, index=False, engine="openpyxl")

print(f"\nExcel con milestones definidas generado: {output_path}")
