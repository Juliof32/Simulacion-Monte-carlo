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

numpy matplotlib imageio pillow

## Estructura del Proyecto

Ver estructura definida en carpetas de secuencial, paralelo, data,
resultados e informe.

## Ejecución

python secuencial/sir_sequential.py\
python paralelo/sir_parallel.py\
python paralelo/run_scaling.py\
python paralelo/make_animation.py

## Comparación

Ambas versiones producen los mismos resultados, pero la paralela reduce
significativamente el tiempo.

## Conclusión

El proyecto valida el uso de Monte Carlo y programación paralela en
simulaciones epidemiológicas.

## Autor

Julio Florentino -- 2025
