import tkinter as tk
from tkinter import filedialog # Importamos la herramienta para buscar archivos 📁
from PIL import Image, ImageTk # Necesitarás instalar pillow: pip install pillow
from tkinter import ttk
from logicaPart1 import calculo_final # Nuestro .py que hace el calculo del area entre curvas

#Captura de la imagen

def seleccionar_archivo():
    ruta = filedialog.askopenfilename()
    if ruta:
        # 1. Abrimos y redimensionamos
        img_original = Image.open(ruta)
        img_redimensionada = img_original.resize((600, 400)) # Ajuste exacto al lienzo
        
        # 2. Convertimos para Tkinter
        # Guardamos la referencia en 'root' para que Python no la borre de la memoria
        root.imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        
        # 3. La ponemos en el lienzo (0,0 es la esquina superior izquierda)
        lienzo.create_image(0, 0, anchor=tk.NW, image=root.imagen_tk)

        global fase_actual
        fase_actual = "calibrando_p1"
        solicitudDimesionesRectangulo.config(text="Paso 1: Haz clic en el origen (esquina inferior izquierda) de la gráfica para calibrarla y tener una precisión correcta.")

#Seleccion actual

fase_actual = "esperando_imagen"
seleccionFuncion="f"

def cambiar_a_f():
    global seleccionFuncion
    seleccionFuncion = "f"
    print("Modo: Seleccionando nodos para f")

def cambiar_a_g():
    global seleccionFuncion
    seleccionFuncion = "g"
    print("Modo: Seleccionando nodos para g")

# Variables para guardar los píxeles de calibración
x_min_px, y_max_px = 0, 400 # Esquina inferior izquierda por defecto
x_max_px, y_min_px = 600, 0 # Esquina superior derecha por defecto

# Variables de control para el flujo secuencial
cantidad_subintervalos_f = 1
tramo_actual_f = 0

cantidad_subintervalos_g = 1
tramo_actual_g = 0

# Estructuras para f
extremos_f = []         # Guardará los (x,y) de los cortes: (a,f(a)), (e,f(e)), etc.
nodos_internos_f = []   # Será una matriz: [[nodos tramo 1], [nodos tramo 2], ...]

# Estructuras para g (las usaremos más adelante)
extremos_g = []
nodos_internos_g = []

#Transformación del nodo tomado

def capturarCoordendas(evento):

    global fase_actual, x_min_px, y_min_px, x_max_px, y_max_px, seleccionFuncion
    x_px = float(evento.x)
    y_px = float(evento.y)
    r = 3
    
    if fase_actual == "esperando_imagen":
        return
    elif fase_actual == "calibrando_p1":
        #Se guarda la esquina inferior izq
        x_min_px = x_px
        y_max_px = y_px
        lienzo.create_oval(x_px - r, y_px - r, x_px + r, y_px + r, fill="red")
        
        fase_actual = "calibrando_p2"
        solicitudDimesionesRectangulo.config(text="Paso 2: Haz clic en la esquina superior derecha de la gráfica.")
    elif fase_actual == "calibrando_p2":
        # Guardamos la esquina superior derecha
        x_max_px = x_px
        y_min_px = y_px
        lienzo.create_oval(x_px - r, y_px - r, x_px + r, y_px + r, fill="red")
        
        fase_actual = "esperando_intervalos"
        solicitudDimesionesRectangulo.config(text="Paso 3: Ingresa los valores de [a,b] y [c,d].")
        
        # Se desbloquean las cajas del texto y el boton de confirmación
        valorA.config(state=tk.NORMAL)
        valorB.config(state=tk.NORMAL)
        valorC.config(state=tk.NORMAL)
        valorD.config(state=tk.NORMAL)
        botonConfirmar.config(state=tk.NORMAL)
    elif fase_actual == "capturando_extremos_f":
        # 1. Transformación matemática (la que ya tienes)
        a, b = float(valorA.get()), float(valorB.get())
        c, d = float(valorC.get()), float(valorD.get())
        xReal = a + ((x_px - x_min_px) / (x_max_px - x_min_px)) * (b - a)
        yReal = c + ((y_max_px - y_px) / (y_max_px - y_min_px)) * (d - c)
        
        # 2. Dibujamos y guardamos el extremo (Azul más oscuro o más grande para diferenciarlos)
        lienzo.create_oval(x_px - 4, y_px - 4, x_px + 4, y_px + 4, fill="darkblue")
        extremos_f.append((xReal, yReal))
        
        # 3. Verificamos si ya completó los extremos
        puntos_esperados = cantidad_subintervalos_f + 1
        if len(extremos_f) == puntos_esperados:
            fase_actual = "capturando_internos_f"
            global tramo_actual_f
            tramo_actual_f = 0 # Empezamos con el primer tramo (índice 0)
            solicitudDimesionesRectangulo.config(
                text=f"Paso 6: Marca los nodos internos del Tramo {tramo_actual_f + 1} de 'f'. Luego presiona 'Siguiente Tramo'."
            )
            botonSiguienteTramo.config(state=tk.NORMAL)

    elif fase_actual == "capturando_internos_f":
        # Transformación matemática
        a, b = float(valorA.get()), float(valorB.get())
        c, d = float(valorC.get()), float(valorD.get())
        xReal = a + ((x_px - x_min_px) / (x_max_px - x_min_px)) * (b - a)
        yReal = c + ((y_max_px - y_px) / (y_max_px - y_min_px)) * (d - c)
        
        # Dibujamos y guardamos el nodo interno (Azul claro o normal)
        lienzo.create_oval(x_px - 3, y_px - 3, x_px + 3, y_px + 3, fill="blue")
        nodos_internos_f[tramo_actual_f].append((xReal, yReal))
    elif fase_actual == "capturando_extremos_g":
        a, b = float(valorA.get()), float(valorB.get())
        c, d = float(valorC.get()), float(valorD.get())
        xReal = a + ((x_px - x_min_px) / (x_max_px - x_min_px)) * (b - a)
        yReal = c + ((y_max_px - y_px) / (y_max_px - y_min_px)) * (d - c)
        
        # Color verde oscuro para los extremos de g
        lienzo.create_oval(x_px - 4, y_px - 4, x_px + 4, y_px + 4, fill="darkgreen")
        extremos_g.append((xReal, yReal))
        
        puntos_esperados = cantidad_subintervalos_g + 1
        if len(extremos_g) == puntos_esperados:
            fase_actual = "capturando_internos_g"
            solicitudDimesionesRectangulo.config(
                text=f"Paso 8: Marca los nodos internos del Tramo {tramo_actual_g + 1} de 'g'. Luego presiona 'Siguiente Tramo'."
            )
            botonSiguienteTramo.config(state=tk.NORMAL)
            # Cambiamos la función del botón para que ahora controle a g
            botonSiguienteTramo.config(command=siguiente_tramo_g)

    elif fase_actual == "capturando_internos_g":
        a, b = float(valorA.get()), float(valorB.get())
        c, d = float(valorC.get()), float(valorD.get())
        xReal = a + ((x_px - x_min_px) / (x_max_px - x_min_px)) * (b - a)
        yReal = c + ((y_max_px - y_px) / (y_max_px - y_min_px)) * (d - c)
        
        # Color verde claro para los internos de g
        lienzo.create_oval(x_px - 3, y_px - 3, x_px + 3, y_px + 3, fill="green")
        nodos_internos_g[tramo_actual_g].append((xReal, yReal))

#Verificación de que los campos de los invervalos no esten vacios

def confirmar_intervalos():
    global fase_actual
    try:
        float(valorA.get())
        float(valorB.get())
        float(valorC.get())
        float(valorD.get())
        
        fase_actual = "configurando_subintervalos_f"
        solicitudDimesionesRectangulo.config(text="Paso 4: Define los subintervalos para 'f' y presiona 'Iniciar Captura de f'.")
        
        # Bloqueamos los intervalos globales
        valorA.config(state=tk.DISABLED)
        valorB.config(state=tk.DISABLED)
        valorC.config(state=tk.DISABLED)
        valorD.config(state=tk.DISABLED)
        botonConfirmar.config(state=tk.DISABLED)
        
        # Desbloqueamos las herramientas de f
        combo_subintervalos.config(state="readonly")
        botonIniciarF.config(state=tk.NORMAL)
        
    except ValueError:
        solicitudDimesionesRectangulo.config(text="⚠️ Error: Llena todos los campos [a,b] y [c,d] con números.")

# Captura de datos de f
def iniciar_captura_f():
    global fase_actual, cantidad_subintervalos_f, nodos_internos_f, extremos_f
    
    # 1. Leemos la cantidad de subintervalos
    cantidad_subintervalos_f = int(combo_subintervalos.get())
    
    # 2. Preparamos las listas (limpiamos por si acaso)
    extremos_f = []
    # Crea una lista vacía por cada tramo (ej. si son 3 tramos: [[], [], []])
    nodos_internos_f = [[] for _ in range(cantidad_subintervalos_f)] 
    
    # 3. Cambiamos de fase
    fase_actual = "capturando_extremos_f"
    puntos_esperados = cantidad_subintervalos_f + 1 # Si hay 2 tramos, hay 3 extremos (a, e, b)
    
    solicitudDimesionesRectangulo.config(
        text=f"Paso 5: Marca los {puntos_esperados} extremos de 'f' de izquierda a derecha."
    )

def siguiente_tramo_f():
    global tramo_actual_f, fase_actual
    
    # Si aún nos quedan tramos por llenar en f...
    if tramo_actual_f < cantidad_subintervalos_f - 1:
        tramo_actual_f += 1
        solicitudDimesionesRectangulo.config(
            text=f"Paso 6: Marca los nodos internos del Tramo {tramo_actual_f + 1} de 'f'."
        )
    else:
        # Si ya terminamos todos los tramos de f
        fase_actual = "configurando_subintervalos_g"
        solicitudDimesionesRectangulo.config(
            text="¡Excelente! Terminaste con 'f'. Ahora define los subintervalos para 'g' y presiona Iniciar."
        )
        botonSiguienteTramo.config(state=tk.DISABLED)
        botonIniciarG.config(state=tk.NORMAL)
        
# Capturad e datos de g

def iniciar_captura_g():
    global fase_actual, cantidad_subintervalos_g, nodos_internos_g, extremos_g, tramo_actual_g
    
    cantidad_subintervalos_g = int(combo_subintervalos.get())
    extremos_g = []
    nodos_internos_g = [[] for _ in range(cantidad_subintervalos_g)] 
    tramo_actual_g = 0
    
    fase_actual = "capturando_extremos_g"
    puntos_esperados = cantidad_subintervalos_g + 1 
    
    solicitudDimesionesRectangulo.config(
        text=f"Paso 7: Marca los {puntos_esperados} extremos de 'g' de izquierda a derecha."
    )
    botonIniciarG.config(state=tk.DISABLED) # Bloqueamos el botón para no pulsarlo 2 veces

def siguiente_tramo_g():
    global tramo_actual_g, fase_actual
    
    if tramo_actual_g < cantidad_subintervalos_g - 1:
        tramo_actual_g += 1
        solicitudDimesionesRectangulo.config(
            text=f"Paso 8: Marca los nodos internos del Tramo {tramo_actual_g + 1} de 'g'."
        )
    else:
        fase_actual = "captura_finalizada"
        solicitudDimesionesRectangulo.config(
            text="¡Captura completa! 🥳 Presiona 'Calcular Área' en el panel derecho."
        )
        botonSiguienteTramo.config(state=tk.DISABLED)
        botonCalcular.config(state=tk.NORMAL)

# Calculo del area

def calcular_area_final():
    global extremos_f, extremos_g, nodos_internos_f, nodos_internos_g
    try:
        # Llamamos a tu método mágico
        area_aproximada = calculo_final(extremos_f, extremos_g, nodos_internos_f, nodos_internos_g)
        
        # Actualizamos la interfaz con el resultado
        labelResultado.config(text=f"Área ≈ {area_aproximada:.4f} u²")
        solicitudDimesionesRectangulo.config(text="¡Cálculo finalizado con éxito! 🚀")
        
    except Exception as e:
        labelResultado.config(text="⚠️ Error matemático")
        print(f"Error al calcular el área: {e}")

# ==========================================
# INTERFAZ GRÁFICA (Ventana y Marcos)
# ==========================================

root = tk.Tk()
root.title("Cálculo de Área con Interpolación")
# Hacemos la ventana más ancha para que quepa el panel de control (ej. 1000x600)
root.geometry("1000x600") 

# --- 1. CREACIÓN DE LOS MARCOS PRINCIPALES ---

# Marco Izquierdo (Ocupará el espacio principal para la gráfica)
# expand=True y fill=tk.BOTH hacen que ocupe todo el espacio disponible a la izquierda
marco_izquierdo = tk.Frame(root)
marco_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Marco Derecho (Ocupará el 20% para el panel de control)
marco_derecho = tk.Frame(root, width=250)
marco_derecho.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
# Evitamos que el marco derecho se encoja si no tiene muchos elementos aún
marco_derecho.pack_propagate(False) 


# --- 2. ELEMENTOS DEL MARCO IZQUIERDO ---

# Etiqueta de instrucciones (Ahora vive en marco_izquierdo)
solicitudDimesionesRectangulo = tk.Label(marco_izquierdo, text="Paso 1: Carga una imagen para comenzar.", font=("Arial", 10, "bold"))
solicitudDimesionesRectangulo.pack(pady=10)

# Lienzo para la gráfica (Ahora vive en marco_izquierdo)
lienzo = tk.Canvas(marco_izquierdo, width=600, height=400, bg="white", cursor="cross")
lienzo.pack(pady=10)
lienzo.bind("<Button-1>", capturarCoordendas)

# Botón de carga de imagen (Ahora vive en marco_izquierdo)
botonCargado = tk.Button(marco_izquierdo, text="Cargar Imagen", command=seleccionar_archivo)
botonCargado.pack(pady=10)


# --- 3. ELEMENTOS DEL MARCO DERECHO (Próximo paso) ---
# Aquí pondremos más adelante las entradas de a,b,c,d y los botones de f y g...
tk.Label(marco_derecho, text="Panel de Control", font=("Arial", 12, "bold")).pack(pady=10)

# ==========================================
# SECCIÓN 1: Intervalos Globales
# ==========================================
tk.Label(marco_derecho, text="1. Definir Intervalos [a,b]x[c,d]", font=("Arial", 9, "bold")).pack(pady=(5, 0))

# Usamos un mini-marco para organizar a,b,c,d en cuadrícula
marco_entradas = tk.Frame(marco_derecho)
marco_entradas.pack(pady=5)

tk.Label(marco_entradas, text="a:").grid(row=0, column=0, padx=2, pady=5)
valorA = tk.Entry(marco_entradas, width=5, state=tk.DISABLED)
valorA.grid(row=0, column=1, padx=2, pady=5)

tk.Label(marco_entradas, text="b:").grid(row=0, column=2, padx=2, pady=5)
valorB = tk.Entry(marco_entradas, width=5, state=tk.DISABLED)
valorB.grid(row=0, column=3, padx=2, pady=5)

tk.Label(marco_entradas, text="c:").grid(row=1, column=0, padx=2, pady=5)
valorC = tk.Entry(marco_entradas, width=5, state=tk.DISABLED)
valorC.grid(row=1, column=1, padx=2, pady=5)

tk.Label(marco_entradas, text="d:").grid(row=1, column=2, padx=2, pady=5)
valorD = tk.Entry(marco_entradas, width=5, state=tk.DISABLED)
valorD.grid(row=1, column=3, padx=2, pady=5)

botonConfirmar = tk.Button(marco_derecho, text="Confirmar Intervalos", command=confirmar_intervalos, state=tk.DISABLED)
botonConfirmar.pack(pady=5)

# Botones de control de flujo
marco_controles_flujo = tk.Frame(marco_derecho)
marco_controles_flujo.pack(pady=15)

botonIniciarF = tk.Button(marco_controles_flujo, text="1. Iniciar Captura de f", command=iniciar_captura_f, state=tk.DISABLED, bg="#e6f2ff")
botonIniciarF.pack(fill=tk.X, pady=2)

botonSiguienteTramo = tk.Button(marco_controles_flujo, text="Siguiente Tramo", command=siguiente_tramo_f, state=tk.DISABLED)
botonSiguienteTramo.pack(fill=tk.X, pady=2)

# Este botón lo programaremos en el siguiente paso para 'g'
botonIniciarG = tk.Button(marco_controles_flujo, text="2. Iniciar Captura de g", command=iniciar_captura_g, state=tk.DISABLED, bg="#e6ffe6")
botonIniciarG.pack(fill=tk.X, pady=2)


# ==========================================
# SECCIÓN 3: Subintervalos Dinámicos
# ==========================================
tk.Label(marco_derecho, text="3. Subintervalos", font=("Arial", 9, "bold")).pack(pady=(15, 0))

marco_sub = tk.Frame(marco_derecho)
marco_sub.pack(pady=5)

tk.Label(marco_sub, text="Cantidad:").grid(row=0, column=0, padx=5)
combo_subintervalos = ttk.Combobox(marco_sub, values=["1", "2", "3"], state="readonly", width=5)
combo_subintervalos.current(0) # Inicia en "1"
combo_subintervalos.grid(row=0, column=1, padx=5)

# ==========================================
# SECCIÓN 4: Resultados (Debajo de la Sección 3)
# ==========================================
tk.Label(marco_derecho, text="4. Resultado", font=("Arial", 9, "bold")).pack(pady=(15, 0))

# El Gran Botón de Calcular (inicia bloqueado)
botonCalcular = tk.Button(marco_derecho, text="Calcular Área", command=calcular_area_final, state=tk.DISABLED, bg="#ffe6e6", font=("Arial", 10, "bold"))
botonCalcular.pack(fill=tk.X, pady=5, padx=5)

# Etiqueta grande y azul para mostrar el número
labelResultado = tk.Label(marco_derecho, text="Área: --", font=("Arial", 12, "bold"), fg="blue")
labelResultado.pack(pady=10)

# ==========================================
# BUCLE PRINCIPAL
# ==========================================
root.mainloop()

print("--- DATOS CAPTURADOS ---")
print("Extremos de f:", extremos_f)
print("Nodos internos de f:", nodos_internos_f)
print("Extremos de g:", extremos_g)
print("Nodos internos de g:", nodos_internos_g)