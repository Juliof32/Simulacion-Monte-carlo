import sys
import os
import csv
import time


# parche de ruta (imprescindible en tu proyecto)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)


# imports correctos según tu estructura
from secuencial.Sec_model import run_sequential_simulation
from Paralelo.Parl_model import run_parallel_simulation


# parámetros del experimento
H = 300
W = 300
DAYS = 60
CORES = [1, 2, 4, 8]   


# ejecución y medición de tiempos
results = []

print("Ejecutando experimento de Strong Scaling...\n")

t_seq = run_sequential_simulation(H, W, DAYS)
print(f"Tiempo secuencial: {t_seq:.4f} s")

for c in CORES:
    t_par = run_parallel_simulation(H, W, DAYS)
    speedup = t_seq / t_par if t_par > 0 else 0

    results.append([c, t_par, speedup])

    print(f"Cores: {c} | Tiempo: {t_par:.4f} s | Speed-up: {speedup:.2f}")


# guardar csv
os.makedirs("data", exist_ok=True)

csv_path = "data/scaling_results.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["cores", "tiempo_segundos", "speedup"])
    for r in results:
        writer.writerow(r)

print("\nCSV generado correctamente en:")
print(csv_path)
