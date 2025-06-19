
from ctypes import CDLL
import numpy as np  # ✅ Esta línea es obligatoria

import sys, os
sys.path.append(os.path.abspath("src"))
from src.hho import hho


# Ruta absoluta al wrapper en cec2017real-master
wrapper_path = os.path.join("cec2017real-master", "code", "wrappers")
sys.path.append(wrapper_path)

import cec17  # Ahora sí debería funcionar

# Ruta del .so compilado (Linux)
so_path = os.path.abspath("libcec17_test_func.so")
dll = CDLL(so_path)

# Parámetros de prueba
func_id = 5
dim = 30
n_hawks = 30
max_iter = 500
lb, ub = -100, 100

# Inicializar función CEC2017 desde la librería
cec17.init("HHO", func_id, dim, dll_path=dll)

def fitness(x):
    return cec17.fitness(np.array(x, dtype=np.float64), dim)


best_sol, best_val = hho(fitness, dim=dim, n_hawks=n_hawks, max_iter=max_iter, lb=lb, ub=ub)

print(f"Función F{func_id} (dim {dim}):")
print("Mejor valor encontrado:", best_val)
