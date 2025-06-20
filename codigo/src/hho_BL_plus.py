import numpy as np

# Búsqueda Local: perturbación gaussiana con reducción dinámica y early stopping

def local_search(solution, fitness_func, dim, step_size=0.01, max_trials=10):
    best = solution.copy()
    best_fitness = fitness_func(best)
    no_improve = 0

    for _ in range(max_trials):
        candidate = best + np.random.normal(0, step_size, dim)
        candidate_fitness = fitness_func(candidate)
        if candidate_fitness < best_fitness:
            best = candidate
            best_fitness = candidate_fitness
            no_improve = 0
        else:
            no_improve += 1
            if no_improve >= 3:
                break

    return best, best_fitness

# Harris Hawks Optimization + Búsqueda Local optimizada (sin paralelismo)

def hho(objective_func, dim, n_hawks=30, max_iter=500, lb=-5.12, ub=5.12):
    hawks = np.random.uniform(lb, ub, (n_hawks, dim))
    fitness = [objective_func(ind) for ind in hawks]
    fitness = np.array(fitness)

    rabbit = hawks[np.argmin(fitness)]
    rabbit_fitness = np.min(fitness)

    for t in range(max_iter):
        E0 = 2 * np.random.rand() - 1
        E = 2 * E0 * (1 - t / max_iter)

        for i in range(n_hawks):
            r1, r2 = np.random.rand(), np.random.rand()
            J = 2 * (1 - np.random.rand())

            if abs(E) >= 1:
                rand_hawk = hawks[np.random.randint(n_hawks)]
                hawks[i] = rand_hawk - r1 * abs(rand_hawk - 2 * r2 * hawks[i])
            else:
                if np.random.rand() >= 0.5:
                    if abs(E) >= 0.5:
                        hawks[i] = rabbit - E * abs(J * rabbit - hawks[i])
                    else:
                        hawks[i] = rabbit - E * abs(rabbit - hawks[i])
                else:
                    Y = rabbit - E * abs(J * rabbit - hawks[i])
                    Z = Y + np.random.normal(0, 1, dim)
                    if objective_func(Z) < fitness[i]:
                        hawks[i] = Z

        # Búsqueda local solo para la élite (top 20%) con parámetros dinámicos
        elite_indices = np.argsort(fitness)[:int(0.2 * n_hawks)]
        dynamic_step = 0.01 * (1 - t / max_iter)
        dynamic_trials = max(2, int(10 * (1 - t / max_iter)))

        for i in elite_indices:
            hawks[i], fitness[i] = local_search(hawks[i], objective_func, dim, step_size=dynamic_step, max_trials=dynamic_trials)

        current_best = np.min(fitness)
        if current_best < rabbit_fitness:
            rabbit_fitness = current_best
            rabbit = hawks[np.argmin(fitness)]

    return rabbit, rabbit_fitness
