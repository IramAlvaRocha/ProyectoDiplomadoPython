from io import BytesIO
import tkinter as tk
from tkinter import Scrollbar, ttk, font
from urllib.request import Request, urlopen
import requests
import warnings
from PIL import Image, ImageTk

class Licores():
    def __init__(self) :

        self.ventana_padre = tk.Tk()
        self.ventana_padre.title("PROYECTO FINAL - LICORES")
        self.ventana_padre.geometry("600x400")

        self.ventana_padre.columnconfigure(3, weight=1)
        self.ventana_padre.columnconfigure(1, weight=1)
        self.ventana_padre.columnconfigure(2, weight=1)
        self.ventana_padre.columnconfigure(4, weight=1)
        self.ventana_padre.rowconfigure(6, weight=2)

        self.ventana_padre
                                        
        self.labelframe1 = ttk.LabelFrame(self.ventana_padre, text="Búsqueda")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10, columnspan=5)

        self.labelCiudad = tk.Label(self.labelframe1, text="Nombre de licor:")
        self.labelCiudad.grid(column=0, row=1, padx=5, pady=5, sticky="w")
        self.campoBusqueda = ttk.Entry(self.labelframe1)
        self.campoBusqueda.grid(column=1, row=1, padx=5, pady=5, sticky="w")

        self.btnBuscar = tk.Button(self.labelframe1, text="Buscar", command=self.buscaResultados)
        self.btnBuscar.grid(column=3, row=2, padx=5, pady=5, sticky="e")

        self.lblTotal = tk.Label(self.ventana_padre)
        self.lblTotal.grid(column=0, row=5, padx=5, pady=5, sticky="w")

        columnas = ('id', 'Bebida')
        self.tree = ttk.Treeview(self.ventana_padre, columns=columnas, show='headings')
        self.tree.heading('id', text='Id')
        self.tree.column("id", minwidth=30, width=30, anchor=tk.W)
        self.tree.heading('Bebida', text='Bebida')
        self.tree.column("Bebida", minwidth=80, width=80, anchor=tk.W)
        self.tree.grid(row=7, column=1, columnspan=4, padx=6, pady=5, sticky='nsew')
        self.tree.bind('<<TreeviewSelect>>', self.verDetalle, True)
        
        self.ventana_padre.mainloop()

    def buscaResultados(self):
        licor = self.campoBusqueda.get()
        parametros = {}
        if licor:
            parametros['i'] = licor.lower()

        urlApi = "https://www.thecocktaildb.com/api/json/v1/1/filter.php"
        responseJson = {}
        exError = None
        try:
            warnings.filterwarnings("ignore", message="Unverified HTTPS request")
            responseFBI = requests.get(urlApi, verify=False, params=parametros)
            if responseFBI.status_code != 200:
                raise Exception("Error on FirmInventory : " + responseFBI.reason)
            else:
                responseJson = responseFBI.json()
                self.jsonResultados = responseJson
                self.lblTotal.config(text='Total de resultados: '+str(len(responseJson['drinks'])))
                self.lblTotal.grid(row=6, column=1)
                self.lista = []
                # Clear the treeview list items
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for elemento in responseJson['drinks']:
                    self.lista.append((elemento['idDrink'], elemento['strDrink']))
                count = 0
                for buscado in self.lista:
                    self.tree.insert('', index='end', iid=count, text='', values=buscado)
                    count = count + 1

                scrollbarY = ttk.Scrollbar(self.ventana_padre, orient="vertical", command=self.tree.yview)
                scrollbarY.grid(row=7, column=6, sticky='nse')
                self.tree.configure(yscroll=scrollbarY.set)

        except Exception as e:
            print(e)

    def verDetalle(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        id = str(values[0])
        for drink in self.jsonResultados['drinks']:
            if drink['idDrink'] == id:
                self.mostrarVentanaDetalle(drink)

    def mostrarVentanaDetalle(self, drink):
        detalle = tk.Toplevel(self.ventana_padre)
        detalle.title("Detalle del Licor")
        detalle.geometry("300x200")
        
        lblNombre = tk.Label(detalle, text="Nombre: " + drink['strDrink'])
        lblNombre.pack(padx=10, pady=10)

test = Licores()
