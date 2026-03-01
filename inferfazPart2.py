import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# ==========================================
# VARIABLES GLOBALES Y DATOS POR DEFECTO
# ==========================================
nodos_exterior = [(50, 90), (80, 50), (50, 10), (20, 50), (50, 90)] 
nodos_interior = [(50, 70), (65, 50), (50, 30), (35, 50), (50, 70)] 

# Variables para el flujo customizado
modo_actual = "default" # Puede ser "default" o "custom"
fase_custom = ""        # "exterior" o "interior"
custom_ext = []
custom_int = []

# ==========================================
# FUNCIONES DE CONVERSIÓN DE ESCALA [0, 100]
# ==========================================
def math_a_px(x_real, y_real):
    """Matemáticas -> Píxeles"""
    x_px = (x_real / 100.0) * 600
    y_px = 400 - ((y_real / 100.0) * 400)
    return x_px, y_px

def px_a_math(x_px, y_px):
    """Píxeles -> Matemáticas"""
    x_real = (x_px / 600.0) * 100
    y_real = 100 - ((y_px / 400.0) * 100)
    return x_real, y_real

# ==========================================
# FLUJO 1: POR DEFECTO
# ==========================================
def cargar_imagen_y_nodos():
    try:
        img_original = Image.open("Sin título.png") 
        img_redimensionada = img_original.resize((600, 400))
        root.imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        lienzo.create_image(0, 0, anchor=tk.NW, image=root.imagen_tk)
    except FileNotFoundError:
        lienzo.create_rectangle(0, 0, 600, 400, fill="#e0e0e0")
        lienzo.create_text(300, 200, text="[Imagen default no encontrada]")

    for x, y in nodos_exterior:
        px, py = math_a_px(x, y)
        lienzo.create_oval(px - 4, py - 4, px + 4, py + 4, fill="blue")

    for x, y in nodos_interior:
        px, py = math_a_px(x, y)
        lienzo.create_oval(px - 4, py - 4, px + 4, py + 4, fill="green")

def graficar_curvas():
    lista_ext = nodos_exterior if modo_actual == "default" else custom_ext
    lista_int = nodos_interior if modo_actual == "default" else custom_int

    # Dibujar exterior
    for i in range(len(lista_ext) - 1):
        x1, y1 = math_a_px(*lista_ext[i])
        x2, y2 = math_a_px(*lista_ext[i+1])
        lienzo.create_line(x1, y1, x2, y2, fill="blue", width=2)
        
    # Dibujar interior (si existe)
    if len(lista_int) > 0:
        for i in range(len(lista_int) - 1):
            x1, y1 = math_a_px(*lista_int[i])
            x2, y2 = math_a_px(*lista_int[i+1])
            lienzo.create_line(x1, y1, x2, y2, fill="green", width=2)

    botonGraficar.config(state=tk.DISABLED)
    botonCalcular.config(state=tk.NORMAL)
    labelInfo.config(text="Curvas graficadas. Ahora calcula el área.")

def calcular_area():
    area_mock = 1250.50 
    labelResultado.config(text=f"Área ≈ {area_mock} u²")
    labelInfo.config(text="¡Cálculo finalizado!")
    
    # ¡AQUÍ DESBLOQUEAMOS EL FLUJO PROPIO!
    if modo_actual == "default":
        botonCargarPropia.config(state=tk.NORMAL)
        labelInfo.config(text="Puedes cargar tu propia imagen ahora.")

# ==========================================
# FLUJO 2: IMAGEN PROPIA (CUSTOM)
# ==========================================
def iniciar_flujo_propio():
    global modo_actual, fase_custom, custom_ext, custom_int
    ruta = filedialog.askopenfilename()
    if ruta:
        # Cargamos nueva imagen y limpiamos lienzo
        img_original = Image.open(ruta)
        img_redimensionada = img_original.resize((600, 400))
        root.imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        lienzo.delete("all")
        lienzo.create_image(0, 0, anchor=tk.NW, image=root.imagen_tk)
        
        # Reiniciamos variables
        modo_actual = "custom"
        fase_custom = "exterior"
        custom_ext = []
        custom_int = []
        
        # Actualizamos UI
        labelInfo.config(text="Paso 1: Marca los nodos de la Curva Exterior.\nLuego presiona 'Cerrar Exterior'.")
        botonCargarPropia.config(state=tk.DISABLED)
        botonCalcular.config(state=tk.DISABLED)
        labelResultado.config(text="Área: --")
        
        # Mostramos botones de captura
        botonCerrarExt.pack(fill=tk.X, pady=2)

def capturar_clic(evento):
    global fase_custom
    if modo_actual != "custom" or fase_custom == "listo":
        return # No hacer nada si no estamos capturando

    x_real, y_real = px_a_math(evento.x, evento.y)
    
    if fase_custom == "exterior":
        custom_ext.append((x_real, y_real))
        lienzo.create_oval(evento.x - 4, evento.y - 4, evento.x + 4, evento.y + 4, fill="blue")
    
    elif fase_custom == "interior":
        custom_int.append((x_real, y_real))
        lienzo.create_oval(evento.x - 4, evento.y - 4, evento.x + 4, evento.y + 4, fill="green")

def cerrar_curva_exterior():
    global fase_custom
    if len(custom_ext) > 2:
        # Añadimos el primer punto al final para cerrar el ciclo
        custom_ext.append(custom_ext[0]) 
        fase_custom = "interior"
        
        botonCerrarExt.pack_forget()
        botonCerrarInt.pack(fill=tk.X, pady=2)
        labelInfo.config(text="Paso 2: Marca nodos de la Curva Interior\n(o ciérrala si no hay hueco).")

def cerrar_curva_interior():
    global fase_custom
    if len(custom_int) > 2:
        custom_int.append(custom_int[0]) # Cierra el ciclo
    
    fase_custom = "listo"
    botonCerrarInt.pack_forget()
    botonGraficar.config(state=tk.NORMAL)
    labelInfo.config(text="¡Captura lista! Presiona 'Graficar Curvas'.")

# ==========================================
# INTERFAZ GRÁFICA
# ==========================================
root = tk.Tk()
root.title("Cálculo de Área - Curvas Cerradas")
root.geometry("900x550") 

# --- MARCOS ---
marco_izquierdo = tk.Frame(root)
marco_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

marco_derecho = tk.Frame(root, width=280)
marco_derecho.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
marco_derecho.pack_propagate(False)

# --- PANEL IZQUIERDO ---
tk.Label(marco_izquierdo, text="Gráfica de Curvas Parametrizadas (Escala Fija 100x100)", font=("Arial", 11, "bold")).pack(pady=5)

lienzo = tk.Canvas(marco_izquierdo, width=600, height=400, bg="white", cursor="cross")
lienzo.pack(pady=5)
lienzo.bind("<Button-1>", capturar_clic) # ¡CONECTAMOS EL RATÓN!

# --- PANEL DERECHO ---
tk.Label(marco_derecho, text="Panel de Control", font=("Arial", 12, "bold")).pack(pady=5)

labelInfo = tk.Label(marco_derecho, text="Paso 1: Revisa los nodos default\ny presiona 'Graficar Curvas'.", fg="gray")
labelInfo.pack(pady=10)

botonGraficar = tk.Button(marco_derecho, text="Graficar Curvas", command=graficar_curvas, bg="#e6f2ff", font=("Arial", 10))
botonGraficar.pack(fill=tk.X, pady=5)

botonCalcular = tk.Button(marco_derecho, text="Calcular Área", command=calcular_area, state=tk.DISABLED, bg="#e6ffe6", font=("Arial", 10))
botonCalcular.pack(fill=tk.X, pady=5)

tk.Label(marco_derecho, text="Resultado:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
labelResultado = tk.Label(marco_derecho, text="Área: --", font=("Arial", 12, "bold"), fg="blue")
labelResultado.pack(pady=5)

# --- SECCIÓN: IMAGEN PROPIA ---
tk.Frame(marco_derecho, height=2, bg="gray").pack(fill=tk.X, pady=15) # Línea separadora
tk.Label(marco_derecho, text="Opciones Avanzadas", font=("Arial", 10, "bold")).pack()

botonCargarPropia = tk.Button(marco_derecho, text="Cargar tu propia imagen", command=iniciar_flujo_propio, state=tk.DISABLED)
botonCargarPropia.pack(fill=tk.X, pady=10)

# Botones dinámicos (Ocultos al inicio)
botonCerrarExt = tk.Button(marco_derecho, text="Cerrar Curva Exterior", command=cerrar_curva_exterior, bg="#ccccff")
botonCerrarInt = tk.Button(marco_derecho, text="Cerrar Curva Interior", command=cerrar_curva_interior, bg="#ccffcc")

cargar_imagen_y_nodos()
root.mainloop()