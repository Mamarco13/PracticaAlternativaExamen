import numpy as np

# Búsqueda Local simple: perturbación gaussiana si mejora, con clipping
def local_search(solution, fitness_func, dim, step_size=0.01, max_trials=10, lb=-100, ub=100):
    best = solution.copy()
    best_fitness = fitness_func(best)

    for _ in range(max_trials):
        candidate = best + np.random.normal(0, step_size, dim)
        candidate = np.clip(candidate, lb, ub)  # Asegurar dominio válido
        candidate_fitness = fitness_func(candidate)
        if candidate_fitness < best_fitness:
            best = candidate
            best_fitness = candidate_fitness

    return best, best_fitness

# Harris Hawks Optimization + Búsqueda Local
def hho(objective_func, dim, n_hawks=30, max_iter=500, lb=-100, ub=100):
    hawks = np.random.uniform(lb, ub, (n_hawks, dim))
    fitness = np.array([objective_func(ind) for ind in hawks])
    rabbit = hawks[np.argmin(fitness)]
    rabbit_fitness = np.min(fitness)

    for t in range(max_iter):
        E0 = 2 * np.random.rand() - 1
        E = 2 * E0 * (1 - t / max_iter)

        for i in range(n_hawks):
            r1, r2 = np.random.rand(), np.random.rand()
            J = 2 * (1 - np.random.rand())

            if abs(E) >= 1:
                # Exploración
                rand_hawk = hawks[np.random.randint(n_hawks)]
                hawks[i] = np.clip(rand_hawk - r1 * abs(rand_hawk - 2 * r2 * hawks[i]), lb, ub)
            else:
                # Explotación
                if np.random.rand() >= 0.5:
                    if abs(E) >= 0.5:
                        hawks[i] = np.clip(rabbit - E * abs(J * rabbit - hawks[i]), lb, ub)
                    else:
                        hawks[i] = np.clip(rabbit - E * abs(rabbit - hawks[i]), lb, ub)
                else:
                    Y = rabbit - E * abs(J * rabbit - hawks[i])
                    Z = np.clip(Y + np.random.normal(0, 1, dim), lb, ub)
                    if objective_func(Z) < fitness[i]:
                        hawks[i] = Z

        # Evaluar soluciones con búsqueda local
        for i in range(n_hawks):
            hawks[i], fitness[i] = local_search(hawks[i], objective_func, dim, lb=lb, ub=ub)

        # Actualizar al mejor (conejo)
        current_best = np.min(fitness)
        if current_best < rabbit_fitness:
            rabbit_fitness = current_best
            rabbit = hawks[np.argmin(fitness)]

    return rabbit, rabbit_fitness
