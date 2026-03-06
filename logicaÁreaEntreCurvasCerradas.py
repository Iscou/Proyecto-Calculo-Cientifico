import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def calcular_spline_figura(puntos):
    # Asegurando si la figura es cerrada
    if not np.allclose(puntos[0], puntos[-1]):
        puntos = np.vstack([puntos, puntos[0]])

    x = puntos[:, 0]
    y = puntos[:, 1]

    # Parametro t para realizar la la parametrizacion
    t = np.zeros(len(puntos))
    t[1:] = np.cumsum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))

    # Interpolando Por Spline Cubico Periodico (comprobando la figura cerrada)
    splineCX = CubicSpline(t, x, bc_type='periodic')
    splineCY = CubicSpline(t, y, bc_type='periodic')

    # Perfeccionar puntos para graficar y calcular el area
    tFinal = np.linspace(t[0], t[-1], 1000)
    xFinal = splineCX(tFinal)
    yFinal = splineCY(tFinal)

    # Calcular el area mediante Teorema de Green
    area = 0.5 * np.abs(np.dot(xFinal, np.roll(yFinal, 1)) - np.dot(yFinal, np.roll(xFinal, 1)))

    return xFinal, yFinal, area

def grafica(puntos, x, y, colorF):
    plt.figure(figsize=(8, 6))
    plt.plot(puntos[:, 0], puntos[:, 1], 'ro', label='Puntos originales')
    plt.plot(x, y, 'b-', label='Spline Cúbico Paramétrico')
    plt.fill(x, y, alpha=0.2, color=colorF) # Rellenar la figura
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def main(puntosF, puntosG):

    xF, yF, areaF = calcular_spline_figura(puntosF)
    xG, yG, areaG = calcular_spline_figura(puntosG)

    #grafica(puntosF, xF, yF, 'skyblue')
    #grafica(puntosG, xG, yG, 'green')

    areaTotal = areaF - areaG

    if areaTotal < 0.0:
        areaTotal = areaTotal * (-1)

    return xF, yF, xG, yG, areaTotal