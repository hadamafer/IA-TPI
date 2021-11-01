import tkinter as tk
from PIL import ImageTk

#Creamos un diccionario que nos permmita guardar las coordenadas y el nombre del objeto
posicion = {"x": 0, "y": 0, "img": None}

#Funcion que permite guardar en el diccionario anterior los datos de un objeto sobre el que presionamos con el raton
def imgPress(event):
    posicion["item"] = canvas.find_closest(event.x, event.y)[0]
    posicion["x"] = event.x
    posicion["y"] = event.y

#Funcion que permite reiniciar el diccionario cuando se sulta un objeto para poder usarlo de nuevo
def imgRelease(event):
    posicion["item"] = None
    posicion["x"] = 0
    posicion["y"] = 0

#Funcion que calcula el desplazamiento y usa el metodo move() de Canvas para reposicionar el item.
def imgMotion(event):
    incremento_x = event.x - posicion["x"]
    incremento_y = event.y - posicion["y"]
    canvas.move(posicion["item"], incremento_x, incremento_y)
    posicion["x"] = event.x
    posicion["y"] = event.y

#Creamos nuestra ventana y el canvas.
root = tk.Tk()
canvas = tk.Canvas(width=400, height=400)
canvas.pack(fill="both", expand=True)

#Enlazamos las senales con su correspondiente funcion usando una etiqueta que delimita los objetos sobre los que se aplica
canvas.tag_bind("img", "<ButtonPress-1>", imgPress)
canvas.tag_bind("img", "<ButtonRelease-1>", imgRelease)
canvas.tag_bind("img", "<B1-Motion>", imgMotion)

#Cargamos la imagen, estipulando la etiqueta que decidimos antes
pic = "TT.png"
img = ImageTk.PhotoImage(file=pic)
canvas.create_image(200, 200, anchor=tk.CENTER, image=img, tags="img")

#Lanzamos nuestra app
root.mainloop()