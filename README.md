# Simulación Monte Carlo del Modelo SIR en Grilla 2D (Secuencial vs Paralela)

##  Descripción General del Proyecto

Este proyecto implementa una simulación epidemiológica basada en el
modelo SIR usando Monte Carlo sobre una grilla de 1000×1000 celdas
(1,000,000 de personas). Se comparan versiones secuencial y paralela
durante 365 días.

## Objetivos

-   Implementar modelo SIR secuencial.
-   Paralelizar la simulación por bloques.
-   Medir rendimiento con strong scaling.
-   Visualizar la propagación.
-   Comparar resultados.

## Lenguaje y Tecnologías

-   Python 3.10+
-   NumPy, Matplotlib
-   Multiprocessing
-   ImageIO, Pillow

## Requerimientos

numpy 
matplotlib 
imageio 
pillow

## Estructura del Proyecto

![Texto alternativo](img/image.png)


## Comparación

Sequecial:

Tiempo de simulacion: 27.7s

🔴 Rojo — INFECTADO     🟢 Verde — RECUPERADO    ⚫ Gris oscuro / Negro — MUERTO


![Animación Secuencial](secuencial/Animation/sir_seq_demo.gif)

Paralelo:

Tiempo de simulacion: 26.1

![Animación Paralela](Paralelo/Animation_par/sir_seq_demo.gif)

## Conclusión

El proyecto valida el uso de Monte Carlo y programación paralela en
simulaciones epidemiológicas.

## Autor

Julio Florentino -- 2025
