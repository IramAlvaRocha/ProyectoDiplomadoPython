import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Función de búsqueda de bebidas
def buscar_bebidas():
    # Obtener el nombre del licor ingresado por el usuario
    licor = entry_licor.get().strip()
    # Validación en caso de que no se ingrese un nombre de licor en la búsqueda
    if not licor:
        messagebox.showwarning("Advertencia", "Ingrese un tipo de licor.") # No se está mostrando el mensaje de error
        return

    # Guardar en variable URL la liga del API para extraer la información por licor 
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={licor}"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verifica si la solicitud HTTP realizada a la API fue exitosa
    if response.status_code != 200:
        messagebox.showerror("Error", "No se pudo obtener información del API.")
        return

    # Obtener la lista de bebidas de la respuesta JSON
    bebidas = response.json().get("drinks", [])
    
    # Limpiar el Treeview antes de insertar nuevos datos
    tree.delete(*tree.get_children())

    # Actualizar el contador de resultados
    lbl_contador.config(text=f"Total de resultados: {len(bebidas)}")

    # Insertar cada bebida en el Treeview
    for bebida in bebidas:
        tree.insert("", "end", values=(bebida["idDrink"], bebida["strDrink"]))

# Función para mostrar el detalle de la bebida seleccionada
def mostrar_detalle(event):
    # Obtener el elemento seleccionado en el Treeview
    selected_item = tree.selection()
    if not selected_item:
        return

    # Obtener el ID de la bebida seleccionada
    item = tree.item(selected_item)
    bebida_id = item["values"][0]

    # Guardar en variable URL la liga del API para extraer la información por id 
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={bebida_id}"
    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verifica si la solicitud HTTP realizada a la API fue exitosa
    if response.status_code != 200:
        messagebox.showerror("Error", "No se pudo obtener información del API.")
        return

    # Obtener los detalles de la bebida de la respuesta JSON
    bebida = response.json().get("drinks", [])[0]

    # Crear una nueva ventana para mostrar los detalles de la bebida
    top = tk.Toplevel(root)
    top.title(bebida["strDrink"])

    # Crear frames para la disposición en dos columnas
    frame_texto = tk.Frame(top)
    frame_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    frame_imagen = tk.Frame(top)
    frame_imagen.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Mostrar el nombre de la bebida
    lbl_bebida_label = tk.Label(frame_texto, text="Bebida:", anchor=tk.W, font=("Helvetica", 10, "bold"))
    lbl_bebida_label.pack(fill=tk.X)
    lbl_bebida = tk.Label(frame_texto, text=bebida['strDrink'], anchor=tk.W)
    lbl_bebida.pack(fill=tk.X)

    # Mostrar la categoría de la bebida
    lbl_categoria_label = tk.Label(frame_texto, text="Categoría:", anchor=tk.W, font=("Helvetica", 10, "bold"))
    lbl_categoria_label.pack(fill=tk.X)
    lbl_categoria = tk.Label(frame_texto, text=bebida['strCategory'], anchor=tk.W)
    lbl_categoria.pack(fill=tk.X)

    # Mostrar las instrucciones de la bebida
    lbl_instrucciones_label = tk.Label(frame_texto, text="Instrucciones:", anchor=tk.W, font=("Helvetica", 10, "bold"))
    lbl_instrucciones_label.pack(fill=tk.X)
    lbl_instrucciones = tk.Label(frame_texto, text=bebida['strInstructions'], anchor=tk.W, justify=tk.LEFT, wraplength=300)
    lbl_instrucciones.pack(fill=tk.X)

    # Obtener y mostrar los ingredientes de la bebida
    ingredientes = [f"{bebida[f'strIngredient{i}']} ({bebida[f'strMeasure{i}']})"
                    for i in range(1, 16) if bebida[f'strIngredient{i}']]
    lbl_ingredientes_label = tk.Label(frame_texto, text="Ingredientes:", anchor=tk.W, font=("Helvetica", 10, "bold"))
    lbl_ingredientes_label.pack(fill=tk.X)
    lbl_ingredientes = tk.Label(frame_texto, text="\n".join(ingredientes), anchor=tk.W, justify=tk.LEFT)
    lbl_ingredientes.pack(fill=tk.X)

    # Descargar y mostrar la imagen de la bebida si está disponible
    if bebida['strDrinkThumb']:
        response = requests.get(bebida['strDrinkThumb'])
        if response.status_code == 200:
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            lbl_imagen = tk.Label(frame_imagen, image=img_tk)
            lbl_imagen.image = img_tk  # Mantener una referencia de la imagen
            lbl_imagen.pack()

# Crear la ventana principal
root = tk.Tk()
root.title("Buscador de Bebidas")

# Crear el marco para los controles de entrada
frame = tk.Frame(root)
frame.pack(pady=20)

# Etiqueta y campo de entrada para el nombre del licor
lbl_licor = tk.Label(frame, text="Licor:")
lbl_licor.pack(side=tk.LEFT)

entry_licor = tk.Entry(frame)
entry_licor.pack(side=tk.LEFT)

# Botón para buscar bebidas
btn_buscar = tk.Button(frame, text="Buscar", command=buscar_bebidas)
btn_buscar.pack(side=tk.LEFT)

# Crear y configurar el Treeview para mostrar las bebidas
columns = ("id", "bebida")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("id", text="Id")
tree.heading("bebida", text="Bebida")
tree.pack(pady=20)

# Mostrar el contador de resultados
lbl_contador = tk.Label(root, text="Total de resultados: 0")
lbl_contador.pack(side=tk.LEFT, padx=10, pady=10)

# Vincular el evento de doble clic en el Treeview para mostrar detalles de la bebida
tree.bind("<Double-1>", mostrar_detalle)

# Iniciar el bucle principal de la aplicación
root.mainloop()
