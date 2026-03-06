import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math
import numpy as np # Necesitamos numpy para hablar con logicaPart2
from logicaÁreaEntreCurvasCerradas import calcular_spline_figura 

#Variables globales y valores por default

nodos_exterior = [(47.33, 68.0), (43.16, 66.5), (39.0, 62.5), (36.33, 56.75), 
                  (35.83, 51.0), (36.5, 44.75), (39.0, 38.25), (43.66, 34.5), 
                  (50.16, 33.25), (55.0, 37.25), (57.83, 43.25), (58.5, 52.0), 
                  (57.49, 58.5), (55.16, 63.5), (51.5, 66.25), (47.33, 68.0)]

nodos_interior = [(47.0, 63.0), (43.5, 56.5), (40.16, 50.75), (43.5, 44.75), 
                  (47.16, 39.0), (50.83, 45.0), (53.83, 51.0), (50.5, 57.5), 
                  (47.0, 63.0)]

modo_actual = "default" 
fase_custom = ""        
custom_ext = []
custom_int = []

# Variable para guardar el área entre pasos
area_calculada_global = 0.0 

# Funciones matematicas y de escala 

def math_a_px(x_real, y_real):
    x_px = (x_real / 100.0) * 600
    y_px = 400 - ((y_real / 100.0) * 400)
    return x_px, y_px

def px_a_math(x_px, y_px):
    x_real = (x_px / 600.0) * 100
    y_real = 100 - ((y_px / 400.0) * 100)
    return x_real, y_real

def ordenar_puntos_por_angulo(puntos):
    """Ordena los puntos en sentido antihorario respecto a su centroide."""
    if len(puntos) < 3: return puntos
    cx = sum(p[0] for p in puntos) / len(puntos)
    cy = sum(p[1] for p in puntos) / len(puntos)
    def angulo(punto):
        return math.atan2(punto[1] - cy, punto[0] - cx)
    return sorted(puntos, key=angulo)

# Flujo de graficacion y calculo
def cargar_imagen_y_nodos():
    try:
        img_original = Image.open("img\Curvas Cerradas\Sin título.png") 
        img_redimensionada = img_original.resize((600, 400))
        root.imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        lienzo.create_image(0, 0, anchor=tk.NW, image=root.imagen_tk)
    except FileNotFoundError:
        lienzo.create_rectangle(0, 0, 600, 400, fill="#e0e0e0")
        lienzo.create_text(300, 200, text="[Imagen default no encontrada]")

    for x, y in nodos_exterior:
        px, py = math_a_px(x, y)
        lienzo.create_oval(px - 4, py - 4, px + 4, py + 4, fill="blue", tags="nodos")

    for x, y in nodos_interior:
        px, py = math_a_px(x, y)
        lienzo.create_oval(px - 4, py - 4, px + 4, py + 4, fill="green", tags="nodos")

def graficar_curvas():
    global area_calculada_global
    lista_ext = nodos_exterior if modo_actual == "default" else custom_ext
    lista_int = nodos_interior if modo_actual == "default" else custom_int

    # 1. Transformar listas a matrices Numpy para que logicaPart2 no falle
    arr_ext = np.array(lista_ext)
    
    # 2. Obtener los 1000 puntos y el área del EXTERIOR
    xF, yF, areaF = calcular_spline_figura(arr_ext)
    # Volvemos a juntar las X y Y para iterarlas en Tkinter
    puntos_suaves_ext = list(zip(xF, yF)) 

    areaG = 0.0
    puntos_suaves_int = []

    # 3. Validar si hay curva INTERIOR y procesarla
    if len(lista_int) > 2:
        arr_int = np.array(lista_int)
        xG, yG, areaG = calcular_spline_figura(arr_int)
        puntos_suaves_int = list(zip(xG, yG))

    # 4. Guardar área total en memoria para usarla luego
    area_calculada_global = abs(areaF - areaG)

    # 5. Dibujamos el exterior suavizado en el lienzo
    for i in range(len(puntos_suaves_ext) - 1):
        x1, y1 = math_a_px(*puntos_suaves_ext[i])
        x2, y2 = math_a_px(*puntos_suaves_ext[i+1])
        lienzo.create_line(x1, y1, x2, y2, fill="blue", width=2)
        
    # 6. Dibujamos el interior suavizado (si existe)
    for i in range(len(puntos_suaves_int) - 1):
        x1, y1 = math_a_px(*puntos_suaves_int[i])
        x2, y2 = math_a_px(*puntos_suaves_int[i+1])
        lienzo.create_line(x1, y1, x2, y2, fill="green", width=2)

    botonGraficar.config(state=tk.DISABLED)
    botonCalcular.config(state=tk.NORMAL)
    labelInfo.config(text="Curvas suavizadas graficadas.\nAhora calcula el área.")

def calcular_area():
    # Solo mostramos la variable que calculamos en la función anterior
    labelResultado.config(text=f"Área ≈ {area_calculada_global:.4f} u²")
    labelInfo.config(text="¡Cálculo finalizado con éxito! ")
    
    if modo_actual == "default":
        botonCargarPropia.config(state=tk.NORMAL)
        labelInfo.config(text="¡Puedes cargar tu propia imagen ahora!")

# Flujo de imagen propia (subida por el user)

def iniciar_flujo_propio():
    global modo_actual, fase_custom, custom_ext, custom_int
    ruta = filedialog.askopenfilename()
    if ruta:
        img_original = Image.open(ruta)
        img_redimensionada = img_original.resize((600, 400))
        root.imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        lienzo.delete("all")
        lienzo.create_image(0, 0, anchor=tk.NW, image=root.imagen_tk)
        
        modo_actual = "custom"
        fase_custom = "exterior"
        custom_ext = []
        custom_int = []
        
        labelInfo.config(text="Paso 1: Marca los nodos de la Curva Exterior.\nLuego presiona 'Cerrar Exterior'.")
        botonCargarPropia.config(state=tk.DISABLED)
        botonCalcular.config(state=tk.DISABLED)
        labelResultado.config(text="Área: --")
        
        botonCerrarExt.pack(fill=tk.X, pady=2)

def capturar_clic(evento):
    global fase_custom
    if modo_actual != "custom" or fase_custom == "listo": return

    x_real, y_real = px_a_math(evento.x, evento.y)
    
    if fase_custom == "exterior":
        custom_ext.append((x_real, y_real))
        lienzo.create_oval(evento.x - 4, evento.y - 4, evento.x + 4, evento.y + 4, fill="blue")
    
    elif fase_custom == "interior":
        custom_int.append((x_real, y_real))
        lienzo.create_oval(evento.x - 4, evento.y - 4, evento.x + 4, evento.y + 4, fill="green")

def cerrar_curva_exterior():
    global fase_custom, custom_ext
    if len(custom_ext) > 2:
        custom_ext = ordenar_puntos_por_angulo(custom_ext)
        custom_ext.append(custom_ext[0]) 
        fase_custom = "interior"
        
        botonCerrarExt.pack_forget()
        botonCerrarInt.pack(fill=tk.X, pady=2)
        labelInfo.config(text="Paso 2: Marca nodos de la Curva Interior\n(o ciérrala si no hay hueco).")

def cerrar_curva_interior():
    global fase_custom, custom_int
    if len(custom_int) > 2:
        custom_int = ordenar_puntos_por_angulo(custom_int)
        custom_int.append(custom_int[0]) 
    
    fase_custom = "listo"
    botonCerrarInt.pack_forget()
    botonGraficar.config(state=tk.NORMAL)
    labelInfo.config(text="¡Captura lista! Presiona 'Graficar Curvas'.")

# Interfaz grafica

root = tk.Tk()
root.title("Cálculo de Área - Curvas Cerradas con Splines")
root.geometry("900x550") 

marco_izquierdo = tk.Frame(root)
marco_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

marco_derecho = tk.Frame(root, width=280)
marco_derecho.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
marco_derecho.pack_propagate(False)

tk.Label(marco_izquierdo, text="Gráfica de Curvas Parametrizadas (Escala Fija 100x100)", font=("Arial", 11, "bold")).pack(pady=5)
lienzo = tk.Canvas(marco_izquierdo, width=600, height=400, bg="white", cursor="cross")
lienzo.pack(pady=5)
lienzo.bind("<Button-1>", capturar_clic) 

tk.Label(marco_derecho, text="Panel de Control", font=("Arial", 12, "bold")).pack(pady=5)
labelInfo = tk.Label(marco_derecho, text="Paso 1: Revisa los nodos default\ny presiona 'Graficar Curvas'.", fg="gray")
labelInfo.pack(pady=10)

botonGraficar = tk.Button(marco_derecho, text="Graficar Curvas Suaves", command=graficar_curvas, bg="#e6f2ff", font=("Arial", 10))
botonGraficar.pack(fill=tk.X, pady=5)

botonCalcular = tk.Button(marco_derecho, text="Calcular Área Exacta", command=calcular_area, state=tk.DISABLED, bg="#e6ffe6", font=("Arial", 10))
botonCalcular.pack(fill=tk.X, pady=5)

tk.Label(marco_derecho, text="Resultado:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
labelResultado = tk.Label(marco_derecho, text="Área: --", font=("Arial", 12, "bold"), fg="blue")
labelResultado.pack(pady=5)

tk.Frame(marco_derecho, height=2, bg="gray").pack(fill=tk.X, pady=15) 
tk.Label(marco_derecho, text="Opciones Avanzadas", font=("Arial", 10, "bold")).pack()

botonCargarPropia = tk.Button(marco_derecho, text="Cargar tu propia imagen", command=iniciar_flujo_propio, state=tk.DISABLED)
botonCargarPropia.pack(fill=tk.X, pady=10)

botonCerrarExt = tk.Button(marco_derecho, text="Cerrar Curva Exterior", command=cerrar_curva_exterior, bg="#ccccff")
botonCerrarInt = tk.Button(marco_derecho, text="Cerrar Curva Interior", command=cerrar_curva_interior, bg="#ccffcc")

cargar_imagen_y_nodos()
root.mainloop()