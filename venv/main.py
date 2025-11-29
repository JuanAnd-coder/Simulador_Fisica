# main.py
"""
Ejemplos y escenarios base para el simulador.
Ejecutar: python main.py
"""

from fisica import Carga
from visual import dibujar_campo_y_potencial
import argparse

def escenario_dipolo():
    cargas = [
        Carga(+2e-9, -0.5, 0.0, nombre="q+"),
        Carga(-2e-9, +0.5, 0.0, nombre="q-"),
    ]
    dibujar_campo_y_potencial(cargas, xmin=-1.2, xmax=1.2, ymin=-1.2, ymax=1.2, nx=120, ny=120, titulo="Dipolo (ejemplo)")

def escenario_memoria_celda():
    # placas paralelas como modelo simplificado de celda capacitor
    cargas = [
        Carga(+1.5e-8, -0.3, 0.0, nombre="placa+"),
        Carga(-1.5e-8, +0.3, 0.0, nombre="placa-"),
    ]
    dibujar_campo_y_potencial(cargas, xmin=-1.0, xmax=1.0, ymin=-0.6, ymax=0.6, nx=150, ny=80, titulo="Celda memoria (modelo capacitor)")

def escenario_transistor_simple():
    # modelo muy simplificado: puerta con carga, canal neutral representado por distribucion
    cargas = [
        Carga(+3e-9, 0.0, 0.6, nombre="puerta"),   # compuerta
        Carga(-1.0e-9, -0.4, -0.6, nombre="fuente"),
        Carga(-1.0e-9, 0.4, -0.6, nombre="drenador"),
    ]
    dibujar_campo_y_potencial(cargas, xmin=-1.0, xmax=1.0, ymin=-1.0, ymax=1.0, nx=160, ny=160, titulo="Transistor (modelo simplificado)")

def main():
    parser = argparse.ArgumentParser(description="Simulador - ejemplos")
    parser.add_argument('--escenario', type=str, choices=['dipolo','memoria','transistor'], default='dipolo')
    args = parser.parse_args()
    if args.escenario == 'dipolo':
        escenario_dipolo()
    elif args.escenario == 'memoria':
        escenario_memoria_celda()
    elif args.escenario == 'transistor':
        escenario_transistor_simple()

if __name__ == "__main__":
    main()
