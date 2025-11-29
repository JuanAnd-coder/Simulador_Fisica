# fisica.py
"""
Funciones físicas básicas para el simulador de campos eléctricos.
"""

import numpy as np

k = 8.9875517923e9  # Constante de Coulomb (N·m^2 / C^2)
EPS = 1e-9          # radio mínimo para evitar singularidad

class Carga:
    def __init__(self, q: float, x: float, y: float, nombre: str = ""):
        """
        q: carga en Coulombs (float)
        x, y: posición en metros (float)
        nombre: etiqueta opcional
        """
        self.q = float(q)
        self.pos = np.array([float(x), float(y)], dtype=float)
        self.nombre = nombre

    def __repr__(self):
        return f"Carga(q={self.q}, pos=({self.pos[0]:.3e},{self.pos[1]:.3e}), name='{self.nombre}')"

def campo_electrico_por_carga(carga: Carga, punto: np.ndarray) -> np.ndarray:
    """
    Campo eléctrico vectorial generado por 'carga' evaluado en 'punto'.
    punto: array-like [x,y]
    devuelve: np.array([Ex, Ey])
    """
    r_vec = np.asarray(punto, dtype=float) - carga.pos
    r = np.linalg.norm(r_vec)
    if r < EPS:
        # evita división por cero: devuelve vector pequeño
        return np.array([0.0, 0.0])
    # E = k*q * r_vec / r^3  (equivalente a k*q/(r^2) * r_hat)
    return k * carga.q * r_vec / (r**3)

def potencial_por_carga(carga: Carga, punto: np.ndarray) -> float:
    r = np.linalg.norm(np.asarray(punto, dtype=float) - carga.pos)
    if r < EPS:
        return k * carga.q / EPS
    return k * carga.q / r

def campo_total(cargas: list, puntos: np.ndarray) -> np.ndarray:
    """
    Calcula el campo total en una lista de puntos.
    cargas: lista de objetos Carga
    puntos: array de forma (N,2)
    devuelve: array (N,2) con [Ex, Ey] en cada punto
    """
    puntos = np.asarray(puntos, dtype=float).reshape(-1, 2)
    N = puntos.shape[0]
    E_total = np.zeros((N, 2), dtype=float)
    for carga in cargas:
        # vectorizado por carga: r_vec para todos los puntos
        r_vecs = puntos - carga.pos  # (N,2)
        rs = np.linalg.norm(r_vecs, axis=1)
        mask = rs >= EPS
        # calcular solo donde no son cercanos a la carga
        # E = k*q * r_vec / r^3
        r3 = np.where(mask, rs**3, EPS**3)
        E = (k * carga.q) * (r_vecs / r3[:, None])
        # si rs < EPS, dejamos E ~ 0 (o podriamos saturar)
        E_total += np.where(mask[:, None], E, 0.0)
    return E_total

def potencial_total(cargas: list, puntos: np.ndarray) -> np.ndarray:
    """
    Calcula el potencial total en una lista de puntos.
    devuelve: array (N,) con V en cada punto
    """
    puntos = np.asarray(puntos, dtype=float).reshape(-1, 2)
    N = puntos.shape[0]
    V_total = np.zeros(N, dtype=float)
    for carga in cargas:
        rs = np.linalg.norm(puntos - carga.pos, axis=1)
        rs = np.where(rs < EPS, EPS, rs)
        V_total += k * carga.q / rs
    return V_total
