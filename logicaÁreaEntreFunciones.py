import numpy as np
from scipy.integrate import quad

# Newton Incremental 
def diferencias_divididas(x, y):
    coef = []
    x_historial = []
    
    for i in range(len(x)):
        x_new = x[i]
        y_new = y[i]
        
        # Caso base: el primer coeficiente es simplemente y0
        if i == 0:
            coef.append(y_new)
        else:
            #  Evaluar el polinomio anterior en el nuevo x 
            p_val = evaluar_newton(coef, x_historial, x_new)
            
            #  Calcular la productoria del denominador 
            productoria = 1.0
            for x_k in x_historial:
                productoria *= (x_new - x_k)
                
            #  Hallar el nuevo coeficiente c_n 
            c_new = (y_new - p_val) / productoria
            coef.append(c_new)
            
        x_historial.append(x_new)
        
    return np.array(coef)

# Evaluación algorítmica 
def evaluar_newton(coef, x_data, x_val):
    n = len(coef) - 1
    p = coef[n]

    for k in range(1, n + 1):
        p = coef[n - k] + (x_val - x_data[n - k]) * p
    return p

# Cálculo de área por tramos
def calcular_area(extremos, lista_internos=[]):
    area = 0
    
    for i in range(len(extremos) - 1):
        extremo_izq = extremos[i]
        extremo_der = extremos[i+1]
        
        # Prevención de errores si lista_internos no tiene sublistas para todos los tramos
        internos = lista_internos[i] if i < len(lista_internos) else []
        
        # Unir todos los nodos del tramo
        nodos_tramo = [extremo_izq, extremo_der] + internos
        
        # Para integrar sí necesitamos saber quién es el inicio y el fin del tramo.
        limites = sorted([extremo_izq[0], extremo_der[0]])
        
        x_n = np.array([p[0] for p in nodos_tramo])
        y_n = np.array([p[1] for p in nodos_tramo])
        
        # Calcular Polinomio de Newton Incrementalmente
        coef = diferencias_divididas(x_n, y_n)
        f_poly = lambda x: evaluar_newton(coef, x_n, x)
        
        # Integrar para hallar el área del tramo
        area_tramo, _ = quad(f_poly, limites[0], limites[1])
        area += area_tramo

    return area

# Cálculo final 
def calculo_final(extremos_f, extremos_g, nodos_internos_f, nodos_internos_g):
    area_total = calcular_area(extremos_f, nodos_internos_f) - calcular_area(extremos_g, nodos_internos_g)

    if area_total < 0.0:
        area_total = area_total * (-1)

    return area_total