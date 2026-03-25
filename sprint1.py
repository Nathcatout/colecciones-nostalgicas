from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# -----------------------------
# DATA LAYER
# -----------------------------

@dataclass
class Elemento:
    nombre: str
    anio: str
    estado: str


# -----------------------------
# LOGIC LAYER
# -----------------------------

class ColeccionService:

    def __init__(self):
        self.colecciones = {}

    def crear_categoria(self, nombre):

        if not nombre:
            raise ValueError("Ingrese un nombre de categoría")

        if nombre in self.colecciones:
            raise ValueError("La categoría ya existe")

        self.colecciones[nombre] = []

    def obtener_categorias(self):
        return list(self.colecciones.keys())

    def agregar_elemento(self, categoria, nombre, anio, estado):

        if categoria not in self.colecciones:
            raise ValueError("Categoría no encontrada")

        elemento = Elemento(nombre, anio, estado)

        self.colecciones[categoria].append(elemento)


# -----------------------------
# GUI
# -----------------------------

class App:

    def __init__(self, root):

        self.root = root
        self.root.title("NostalgiaHub - Sprint 1")
        self.root.geometry("500x420")

        self.service = ColeccionService()

        titulo = tk.Label(
            root,
            text="Gestión de Colecciones Nostálgicas",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        # -----------------------------
        # CREAR CATEGORIA
        # -----------------------------

        frame_cat = tk.LabelFrame(root, text="Crear Categoría", padx=10, pady=10)
        frame_cat.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_cat, text="Nombre").grid(row=0, column=0)

        self.entry_categoria = tk.Entry(frame_cat, width=30)
        self.entry_categoria.grid(row=0, column=1, padx=5)

        tk.Button(
            frame_cat,
            text="Crear",
            command=self.crear_categoria
        ).grid(row=0, column=2)

        self.lista_categorias = tk.Listbox(frame_cat, height=5)
        self.lista_categorias.grid(row=1, column=0, columnspan=3, pady=10, sticky="we")

        # seleccionar categoría desde lista
        self.lista_categorias.bind("<<ListboxSelect>>", self.seleccionar_categoria)

        # -----------------------------
        # AGREGAR ELEMENTO
        # -----------------------------

        frame_elem = tk.LabelFrame(root, text="Agregar Elemento", padx=10, pady=10)
        frame_elem.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_elem, text="Categoría").grid(row=0, column=0)

        self.cat = tk.Entry(frame_elem)
        self.cat.grid(row=0, column=1)

        tk.Label(frame_elem, text="Nombre").grid(row=1, column=0)

        self.nombre = tk.Entry(frame_elem)
        self.nombre.grid(row=1, column=1)

        tk.Label(frame_elem, text="Año").grid(row=2, column=0)

        self.anio = tk.Entry(frame_elem)
        self.anio.grid(row=2, column=1)

        tk.Label(frame_elem, text="Estado").grid(row=3, column=0)

        self.estado = ttk.Combobox(
            frame_elem,
            values=["Excelente", "Bueno", "Regular", "Deteriorado"],
            state="readonly"
        )
        self.estado.grid(row=3, column=1)
        self.estado.set("Bueno")

        tk.Button(
            frame_elem,
            text="Agregar elemento",
            command=self.agregar
        ).grid(row=4, column=0, columnspan=2, pady=5)

    # -----------------------------
    # FUNCIONES
    # -----------------------------

    def crear_categoria(self):

        try:

            nombre = self.entry_categoria.get().strip()

            self.service.crear_categoria(nombre)

            self.entry_categoria.delete(0, tk.END)

            self.actualizar_lista()

            messagebox.showinfo("Éxito", "Categoría creada")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista(self):

        self.lista_categorias.delete(0, tk.END)

        for cat in self.service.obtener_categorias():
            self.lista_categorias.insert(tk.END, cat)

    def seleccionar_categoria(self, event):

        seleccion = self.lista_categorias.curselection()

        if not seleccion:
            return

        categoria = self.lista_categorias.get(seleccion)

        self.cat.delete(0, tk.END)
        self.cat.insert(0, categoria)

    def agregar(self):

        try:

            self.service.agregar_elemento(
                self.cat.get(),
                self.nombre.get(),
                self.anio.get(),
                self.estado.get()
            )

            messagebox.showinfo("Éxito", "Elemento agregado")

            self.nombre.delete(0, tk.END)
            self.anio.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))


# -----------------------------
# MAIN
# -----------------------------

root = tk.Tk()
app = App(root)
root.mainloop()