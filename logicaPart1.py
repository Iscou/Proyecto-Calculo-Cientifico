import numpy as np
from scipy.integrate import quad


# Tablas divididas
def diferencias_divididas(x, y):
    
    n = len(y)
    coef = np.zeros([n, n])
    coef[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            coef[i, j] = (coef[i+1, j-1] - coef[i, j-1]) / (x[i+j] - x[i])

    # Retorna solo los coeficientes de la diagonal superior
    return coef[0, :]

def evaluar_newton(coef, x_data, x_val):
    # Evaluar polinomio en un punto x_val
    n = len(coef) - 1
    p = coef[n]

    for k in range(1, n + 1):
        p = coef[n - k] + (x_val - x_data[n - k]) * p
    return p

def calcular_area(extremos, lista_internos=[]):
    area = 0
    
    # Iteramos sobre los intervalos (si hay 4 puntos de intervalo, hay 3 tramos)
    for i in range(len(extremos) - 1):
        # Definir extremos del tramo actual
        extremo_izq = extremos[i]
        extremo_der = extremos[i+1]
        internos = lista_internos[i]
        
        # Consolidar todos los nodos del tramo y ordenar por X
        nodos_tramo = sorted([extremo_izq, extremo_der] + internos, key=lambda p: p[0])
        x_n = np.array([p[0] for p in nodos_tramo])
        y_n = np.array([p[1] for p in nodos_tramo])
        
        # Calcular Polinomio de Newton
        coef = diferencias_divididas(x_n, y_n)
        f_poly = lambda x: evaluar_newton(coef, x_n, x)
        
        # Integrar para hallar el área del tramo
        area_tramo, _ = quad(f_poly, x_n[0], x_n[-1])
        area += area_tramo

    return area

# Recibe los tramos
def calculo_final(extremos_f, extremos_g, nodos_internos_f, nodos_internos_g):

    area_total = calcular_area(extremos_f, nodos_internos_f) - calcular_area(extremos_g, nodos_internos_g)

    if area_total < 0.0:
        area_total = area_total * (-1)

    return area_total

