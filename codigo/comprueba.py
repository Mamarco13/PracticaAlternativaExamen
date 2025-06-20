import pandas as pd

# Cargar archivo generado
df = pd.read_excel("results_cec_batch/cec2017_ALL_algorithms.xlsx")

# Separar funciones
func_cols = [col for col in df.columns if col.startswith("F")]
algorithms = df["alg"].unique()

print("🔍 Diagnóstico por algoritmo y función:\n")

for alg in algorithms:
    print(f"🔧 Algoritmo: {alg}")
    df_alg = df[df["alg"] == alg]
    for f in func_cols:
        vals = df_alg[f]
        if (vals == 1e10).all():
            print(f"  ❌ {f}: TODAS las ejecuciones son 1e10 (probable fallo)")
        elif vals.std() < 1e-8:
            print(f"  ⚠️ {f}: Varianza extremadamente baja (posible estancamiento)")
    print("")
