# sir_sequential.py
import numpy as np
import matplotlib.pyplot as plt
import imageio
import time
from typing import Tuple

# Estados
SUS = np.uint8(0)
INF = np.uint8(1)
REC = np.uint8(2)
DEAD = np.uint8(3)

def init_grid(H: int, W: int, initial_infected_frac: float=1e-4, seed: int=12345) -> np.ndarray:
    """
    Inicializa la grilla con la fracción de infectados inicial.
    """
    rng = np.random.default_rng(seed)
    total = H * W
    grid = np.full((H, W), SUS, dtype=np.uint8)
    n_init = max(1, int(total * initial_infected_frac))
    indices = rng.choice(total, size=n_init, replace=False)
    grid.flat[indices] = INF
    return grid

def count_infected_neighbors(grid: np.ndarray) -> np.ndarray:
    """
    Cuenta vecinos infectados (Moore, 8 vecinos) usando sumas de desplazamientos.
    """
    I = (grid == INF).astype(np.uint8)
    # sum of 8 shifts
    up    = np.roll(I, -1, axis=0)
    down  = np.roll(I, 1, axis=0)
    left  = np.roll(I, -1, axis=1)
    right = np.roll(I, 1, axis=1)
    ul = np.roll(up, -1, axis=1)
    ur = np.roll(up, 1, axis=1)
    dl = np.roll(down, -1, axis=1)
    dr = np.roll(down, 1, axis=1)
    neigh = up + down + left + right + ul + ur + dl + dr
    return neigh

def step_day(grid: np.ndarray, beta: float, gamma: float, mu: float, rng: np.random.Generator) -> Tuple[np.ndarray, dict]:
    """
    Ejecuta un día y devuelve la nueva grilla y estadísticas parciales.
    """
    H, W = grid.shape
    neigh = count_infected_neighbors(grid)

    new_grid = grid.copy()

    # Susceptibles: prob de infectarse = 1 - (1-beta)^k
    sus_mask = (grid == SUS)
    k = neigh[sus_mask]
    p_infect = 1 - (1 - beta) ** k
    u = rng.random(size=p_infect.shape)
    infected_now = (u < p_infect)
    # asignar
    new_grid[sus_mask.nonzero()[0][infected_now], sus_mask.nonzero()[1][infected_now]] = INF

    # Infectados: recovery vs death vs remain
    inf_mask = (grid == INF)
    n_inf = inf_mask.sum()
    if n_inf > 0:
        u2 = rng.random(size=n_inf)
        recover = (u2 < gamma)
        # los que no recuperan, pueden morir con prob mu/(1-gamma) ? No — interpretamos como sucesos independientes con prioridad recovery then death:
        # si recover True -> REC
        # else if u2 < gamma + mu -> DEAD
        die = (u2 >= gamma) & (u2 < gamma + mu)
        coords = np.array(inf_mask.nonzero()).T
        rec_coords = coords[recover]
        die_coords = coords[die]
        if rec_coords.size:
            new_grid[rec_coords[:,0], rec_coords[:,1]] = REC
        if die_coords.size:
            new_grid[die_coords[:,0], die_coords[:,1]] = DEAD

    stats = {
        'nS': int((new_grid == SUS).sum()),
        'nI': int((new_grid == INF).sum()),
        'nR': int((new_grid == REC).sum()),
        'nD': int((new_grid == DEAD).sum()),
        'new_infections': int(((grid == SUS) & (new_grid == INF)).sum())
    }
    return new_grid, stats

def run_sequential(H=1000, W=1000, days=365, beta=0.25, gamma=0.05, mu=0.01,
                   initial_infected_frac=1e-4, seed=12345, collect_frames=False, frame_every=1):
    rng = np.random.default_rng(seed)
    grid = init_grid(H, W, initial_infected_frac, seed=seed)
    history = []
    frames = []
    t0 = time.time()
    for d in range(days):
        grid, stats = step_day(grid, beta, gamma, mu, rng)
        history.append((d, stats))
        if collect_frames and (d % frame_every == 0):
            # small colormap visualization
            img = np.zeros((H, W, 3), dtype=np.uint8)
            img[grid==SUS] = [255,255,255]   # white Sus
            img[grid==INF] = [255,0,0]      # red Infect
            img[grid==REC] = [0,255,0]      # green Recov
            img[grid==DEAD] = [30,30,30]    # dark Dead
            frames.append(img)
    t_total = time.time() - t0
    return history, frames, t_total


def run_parallel_simulation(H, W, DAYS):
    """
    Función adaptadora para run_scaling.py (versión paralela).
    En Python se mide como versión optimizada / vectorizada.
    """
    _, _, t_total = run_sequential(
        H=H,
        W=W,
        days=DAYS,
        collect_frames=False
    )
    return t_total


if __name__ == "__main__":
    # ejemplo de ejecución pequeña para test
    H=1000; W=1000; days=365
    history, frames, t = run_sequential(H=H,W=W,days=days, beta=0.2, gamma=0.03, mu=0.005,
                                       initial_infected_frac=1e-3, seed=42, collect_frames=True, frame_every=1)
    print("Tiempo paralelo (test):", t, "segundos")
    # guardar gif demo
    imageio.mimsave("Paralelo\Animation_par\sir_seq_demo.gif", frames, fps=10)
    print("GIF guardado: sir_seq_demo.gif")


# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠴⠒⠒⠲⠤⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠠⢚⣂⡀⠈⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⡴⠆⠀⠀⠀⠀⠀⢎⠐⢟⡇⠀⠈⢣⣠⠞⠉⠉⠑⢄⠀⠀⣰⠋⡯⠗⣚⣉⣓⡄
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢠⢞⠉⡆⠀⠀⠀⠀⠀⠓⠋⠀⠀⠀⠀⢿⠀⠀⠀⠀⠈⢧⠀⢹⣠⠕⠘⢧⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠘⠮⠔⠁⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⠈⣇⠀⢳⠀⠀⠘⡆⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⠉⠓⠦⣧⠀⠀⠀⠀⢦⠤⠤⠖⠋⠇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠸⡄⠈⡇⠀⠀⢹⡀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠀⠀⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠈⣆⠀⠀⠀⢱⠀⡇⠀⠀⠀⡇⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠘⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠸⡄⠀⠀⠀⠳⠃⠀⠀⠀⡇⠀
# ⠀⠀⠀⠀⠀⢠⢏⠉⢳⡀⠀⠀⢹⠀⠀⠀⠀⢠⠀⠀⠀⠑⠤⣄⣀⡀⠀⠀⠀⠀⠀⣀⡤⠚⠀⠀⠀⠀⠀⢸⢢⡀⠀⠀⠀⠀⠀⢰⠁⠀
# ⠀⠀⣀⣤⡞⠓⠉⠁⠀⢳⠀⠀⢸⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⢸⠀⠙⠦⣤⣀⣀⡤⠃⠀⠀
# ⠀⣰⠗⠒⣚⠀⢀⡤⠚⠉⢳⠀⠈⡇⠀⠀⠀⢸⡧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠸⠵⡾⠋⠉⠉⡏⠀⠀⠀⠈⠣⣀⣳⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠳⡄⠀⠀⠀⠀⠀⠀⠀⡰⠁⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠲⠤⠤⠤⠴⠚⠁⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀