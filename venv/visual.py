# visual.py
"""
Funciones de visualización: líneas de campo (streamplot), flechas y mapa de potencial.
"""

import numpy as np
import matplotlib.pyplot as plt
from fisica import campo_total, potencial_total, Carga

def generar_cuadricula(xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5, nx=50, ny=50):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    X, Y = np.meshgrid(x, y)
    puntos = np.vstack([X.ravel(), Y.ravel()]).T  # (nx*ny, 2)
    return X, Y, puntos

def dibujar_campo_y_potencial(cargas, xmin=-1.5, xmax=1.5, ymin=-1.5, ymax=1.5, nx=50, ny=50, mostrar_equipotenciales=True, titulo="Campo eléctrico"):
    """
    Dibuja líneas de campo (streamplot), puntos de carga y mapa de potencial.
    cargas: lista de Carga
    """
    X, Y, puntos = generar_cuadricula(xmin, xmax, ymin, ymax, nx, ny)
    E = campo_total(cargas, puntos)      # (N,2)
    Ex = E[:, 0].reshape(X.shape)
    Ey = E[:, 1].reshape(X.shape)
    magE = np.sqrt(Ex**2 + Ey**2)

    V = potencial_total(cargas, puntos).reshape(X.shape)

    fig, ax = plt.subplots(figsize=(8, 7))
    # Streamplot con color según magnitud (usar log para mejor contraste)
    # evitar valores cero para log
    mag_for_color = np.log10(magE + 1e-12)
    strm = ax.streamplot(X, Y, Ex, Ey, color=mag_for_color, linewidth=1, density=1.2, cmap='plasma', arrowsize=1.5)
    cb = fig.colorbar(strm.lines, ax=ax, label='log10(|E|) (escala)')

    # Dibujar equipotenciales (contour)
    if mostrar_equipotenciales:
        levels = np.linspace(np.nanpercentile(V, 5), np.nanpercentile(V, 95), 12)
        cont = ax.contour(X, Y, V, levels=levels, alpha=0.6, cmap='coolwarm', linestyles='dashed')
        ax.clabel(cont, inline=1, fontsize=8, fmt="%.1e")
    
    # Dibujar cargas
    for c in cargas:
        color = 'red' if c.q > 0 else 'blue'
        ax.scatter(c.pos[0], c.pos[1], s=110, c=color, edgecolors='k')
        ax.text(c.pos[0] + 0.03, c.pos[1] + 0.03, f"{c.nombre}\n{c.q:.1e} C", fontsize=9)

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title(titulo)
    ax.set_aspect('equal', 'box')
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def dibujar_flechas(cargas, nx=20, ny=20, **kwargs):
    X, Y, puntos = generar_cuadricula(nx=nx, ny=ny, **{k:v for k,v in kwargs.items() if k in ['xmin','xmax','ymin','ymax']})
    E = campo_total(cargas, puntos)
    Ex = E[:, 0].reshape(X.shape)
    Ey = E[:, 1].reshape(Y.shape)
    fig, ax = plt.subplots(figsize=(7,7))
    ax.quiver(X, Y, Ex, Ey, scale=1e6)  # escala heurística; ajustar según magnitudes
    for c in cargas:
        color = 'red' if c.q > 0 else 'blue'
        ax.scatter(c.pos[0], c.pos[1], s=100, c=color)
    ax.set_title("Campo eléctrico (quiver)")
    ax.set_aspect('equal')
    plt.show()
