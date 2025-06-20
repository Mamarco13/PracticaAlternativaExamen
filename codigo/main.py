import sys
import os
from ctypes import CDLL
import numpy as np

# Agregar src al path
sys.path.append(os.path.abspath("src"))

# Selección de versión HHO
mode = "--std"
for arg in sys.argv:
    if arg in ("--bl", "--blplus"):
        mode = arg

if mode == "--bl":
    from src.hho_BL import hho
    print("Usando HHO con Búsqueda Local (BL)")
elif mode == "--blplus":
    from src.hho_BL_plus import hho
    print("Usando HHO con Búsqueda Local Optimizada (BL Plus)")
else:
    from src.hho import hho
    print("Usando HHO estándar")

# Ruta del wrapper
wrapper_path = os.path.join("cec2017real-master", "code", "wrappers")
sys.path.append(wrapper_path)
import cec17

# Ruta al .so
so_path = os.path.abspath("libcec17_test_func.so")
dll = CDLL(so_path)

# Parámetros
func_id = 5
dim = 30
n_hawks = 30
max_iter = 500
lb, ub = -100, 100

# Inicializar función
cec17.init("HHO", func_id, dim, dll_path=dll)

# Evaluación
def fitness(x):
    return cec17.fitness(np.array(x, dtype=np.float64), dim)

# Ejecutar optimización
best_sol, best_val = hho(fitness, dim=dim, n_hawks=n_hawks, max_iter=max_iter, lb=lb, ub=ub)

# Mostrar resultados
print(f"Función F{func_id} (dim {dim}):")
print("Mejor valor encontrado:", best_val)
