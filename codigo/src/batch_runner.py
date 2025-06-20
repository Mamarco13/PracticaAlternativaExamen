import os
import sys
import csv
import numpy as np
import shutil
from ctypes import CDLL

# Agregar src al path
sys.path.append(os.path.abspath("src"))

# Selección de versión HHO
mode = "--std"
for arg in sys.argv:
    if arg in ("--bl", "--blplus"):
        mode = arg

if mode == "--bl":
    from hho_BL import hho
    alg_id = "HHOBL"
    print("Usando HHO con Búsqueda Local (BL)")
elif mode == "--blplus":
    from hho_BL_plus import hho
    alg_id = "HHOBLplus"
    print("Usando HHO con Búsqueda Local Optimizada (BLplus)")
else:
    from hho import hho
    alg_id = "HHO"
    print("Usando HHO estándar")

# Añadir ruta del wrapper
sys.path.append("cec2017real-master/code/wrappers")
import cec17

# Configuración
DIM = 30
N_HAWKS = 30
MAX_ITER = 500
N_RUNS = 51
FUNC_IDS = [i for i in range(1, 31) if i != 2]
RESULT_DIR = "results_cec_batch"
WRAPPER_RESULT_DIR = alg_id
SO_NAME = "libcec17_test_func.so"

# Preparar carpetas
shutil.rmtree(WRAPPER_RESULT_DIR, ignore_errors=True)
os.makedirs(WRAPPER_RESULT_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# Cargar .so
dll_path = os.path.abspath(SO_NAME)
dll = CDLL(dll_path)

for fid in FUNC_IDS:
    print(f"Ejecutando F{fid} ({DIM}D)...")
    fitness_values = []

    for run in range(N_RUNS):
        try:
            cec17.init(WRAPPER_RESULT_DIR, fid, DIM, dll_path=dll)

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
            print(f"Error en F{fid}, run {run + 1}: {e}")
            fitness_values.append(np.nan)

    # Guardar CSV
    csv_path = os.path.join(RESULT_DIR, f"F{fid}_results_{alg_id}.csv")
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

print("\n¡Benchmark completado! Resultados guardados como CSV por función y TXT por algoritmo.")
