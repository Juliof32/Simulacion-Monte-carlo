import matplotlib
matplotlib.use("Agg")  
import pandas as pd
import matplotlib.pyplot as plt
import os


# cargar csv
df = pd.read_csv("data/scaling_results.csv")

cores = df["cores"]
tiempo = df["tiempo_segundos"]
speedup = df["speedup"]


# crear carpeta de figuras
os.makedirs("informe/figuras", exist_ok=True)

# gráfica 1: tiempo vs cores
plt.figure()
plt.plot(cores, tiempo, marker="o")
plt.xlabel("Número de Cores")
plt.ylabel("Tiempo (s)")
plt.title("Tiempo vs Cores")
plt.grid(True)
plt.savefig("informe/figuras/tiempo_vs_cores.png")
plt.close()

# gráfica 2: speed-up vs cores
plt.figure()
plt.plot(cores, speedup, marker="o")
plt.xlabel("Número de Cores")
plt.ylabel("Speed-up")
plt.title("Speed-up vs Cores")
plt.grid(True)
plt.savefig("informe/figuras/speedup_vs_cores.png")
plt.close()

# función para limpiar la consola
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")


print("Gráficas generadas correctamente en informe/figuras/")

    
    
print("""

⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣶⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⣀⡀⣠⣾⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⡇⠀⠀⠀⠀
⠀⣶⣿⣦⣜⣿⣿⣿⡟⠻⣿⣿⣿⣿⣿⣿⣿⡿⢿⡏⣴⣺⣦⣙⣿⣷⣄⠀⠀⠀
⠀⣯⡇⣻⣿⣿⣿⣿⣷⣾⣿⣬⣥⣭⣽⣿⣿⣧⣼⡇⣯⣇⣹⣿⣿⣿⣿⣧⠀⠀
⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣷⠀

""")
