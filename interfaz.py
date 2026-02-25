import tkinter as tk
from tkinter import filedialog # Importamos la herramienta para buscar archivos 📁
from PIL import Image, ImageTk # Necesitarás instalar pillow: pip install pillow

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


#Seleccion actual

seleccionActual="f"

def cambiar_a_f():
    global seleccionActual
    seleccionActual = "f"
    print("Modo: Seleccionando nodos para f")

def cambiar_a_g():
    global seleccionActual
    seleccionActual = "g"
    print("Modo: Seleccionando nodos para g")

puntosF=[]
puntosG=[]

#Transformación del nodo tomado

def capturarCoordendas(evento):
        # Hacemos get de los valores de entrada
    a = float(valorA.get())
    b = float(valorB.get())
    c = float(valorC.get())
    d = float(valorD.get())

        # Definimos un radio pequeño para el punto
    r = 3 

    if seleccionActual == "f":
        color = "blue"
    else:
        color = "green"

        # Dibujamos el óvalo en el lienzo
    

        # Coordendas del Click
    x_px = float(evento.x)
    y_px = float(evento.y)

    lienzo.create_oval(x_px - r, y_px - r, x_px + r, y_px + r, fill=color)
    
        #Transformación de la escala
    xReal= a+(x_px/600)*(b-a)
    yReal= d-(y_px/400)*(d-c)

    parOrdenado=(xReal,yReal)
    
    if seleccionActual == "f":
        global puntosF
        puntosF.append(parOrdenado)
    else:
        global puntosG
        puntosG.append(parOrdenado)



# Ventana principal 

root = tk.Tk()
root.title("Calculo de Area aprovechando la Interpolacion")
root.geometry("800x600")

# Elementos Visuales de Cada Ventana

## Boton de cargado de imagen

botonCargado=tk.Button(root, text="Cargar Imagen", command=seleccionar_archivo )
botonCargado.pack(pady=10, side=tk.BOTTOM)

lienzo = tk.Canvas(root,width=600, height=400, bg="white")
lienzo.pack()

lienzo.bind("<Button-1>", capturarCoordendas)

## Cargado de parametros a, b, c y d

    ### Label para solicitar los datos
solicitudDimesionesRectangulo=tk.Label(root, text="Defina como esta definida la funcion f,g: [a,b]->[c,d]:")
solicitudDimesionesRectangulo.pack()

    ###

# Contenedor para el formulario de entradas

marcoEntradas = tk.Frame(root)
marcoEntradas.pack(pady=10)

# Fila 0: a y b (Dominio)
tk.Label(marcoEntradas, text="Valor de a:").grid(row=0, column=0, padx=5, pady=5)
valorA = tk.Entry(marcoEntradas)
valorA.grid(row=0, column=1, padx=5, pady=5)

tk.Label(marcoEntradas, text="Valor de b:").grid(row=0, column=2, padx=5, pady=5)
valorB = tk.Entry(marcoEntradas)
valorB.grid(row=0, column=3, padx=5, pady=5)

# Fila 1: c y d (Rango) - Mismas columnas, siguiente fila
tk.Label(marcoEntradas, text="Valor de c:").grid(row=1, column=0, padx=5, pady=5)
valorC = tk.Entry(marcoEntradas)
valorC.grid(row=1, column=1, padx=5, pady=5)

tk.Label(marcoEntradas, text="Valor de d:").grid(row=1, column=2, padx=5, pady=5)
valorD = tk.Entry(marcoEntradas)
valorD.grid(row=1, column=3, padx=5, pady=5)


botonCambiarF=tk.Button(root, text="Propiedades de f", command=cambiar_a_f)
botonCambiarF.pack()

botonCambiarG=tk.Button(root, text="Propiedades de g", command=cambiar_a_g)
botonCambiarG.pack()

# Bucle principal de la aplicacion

root.mainloop()

print(puntosF)
print(puntosG)