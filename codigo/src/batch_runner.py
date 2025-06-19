import os
import sys
import csv
import numpy as np
from ctypes import CDLL
from hho import hho

# Añadir ruta del wrapper
sys.path.append("cec2017real-master/code/wrappers")
import cec17

# Configuración
DIM = 30
N_HAWKS = 30
MAX_ITER = 500
N_RUNS = 51
FUNC_IDS = [i for i in range(1, 31) if i != 2]  # Saltar F2
RESULT_DIR = "results_cec_batch"
SO_NAME = "libcec17_test_func.so"

# Cargar .so
dll_path = os.path.abspath(SO_NAME)
dll = CDLL(dll_path)

# Crear carpeta resultados si no existe
os.makedirs(RESULT_DIR, exist_ok=True)

for fid in FUNC_IDS:
    print(f"Ejecutando F{fid} ({DIM}D)...")
    fitness_values = []

    for run in range(N_RUNS):
        try:
            cec17.init("HHO", fid, DIM, dll_path=dll)

            def fitness(x):
                return cec17.fitness(np.array(x, dtype=np.float64), DIM)

            best_sol, best_val = hho(
                fitness,
                dim=DIM,
                n_hawks=N_HAWKS,
                max_iter=MAX_ITER,
                lb=-100,
                ub=100
            )
            fitness_values.append(best_val)

        except Exception as e:
            print(f"⚠️ Error en F{fid}, run {run + 1}: {e}")
            fitness_values.append(np.nan)

    # Guardar CSV
    csv_path = os.path.join(RESULT_DIR, f"F{fid}_results.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Run", "Fitness"])
        for i, val in enumerate(fitness_values, 1):
            writer.writerow([i, val])
        writer.writerow([])
        writer.writerow(["Best", np.nanmin(fitness_values)])
        writer.writerow(["Mean", np.nanmean(fitness_values)])
        writer.writerow(["Std", np.nanstd(fitness_values)])

    print(f"F{fid}: Mejor = {np.nanmin(fitness_values):.4f}, Media = {np.nanmean(fitness_values):.4f}")

print("\n¡Benchmark completado! Resultados guardados como CSV por función.")
