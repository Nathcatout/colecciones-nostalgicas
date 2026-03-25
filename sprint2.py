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

    def obtener_elementos(self, categoria):

        if categoria not in self.colecciones:
            raise ValueError("Categoría no encontrada")

        return self.colecciones[categoria]

    def editar_elemento(self, categoria, indice, nombre, anio, estado):

        self.colecciones[categoria][indice] = Elemento(nombre, anio, estado)


# -----------------------------
# GUI
# -----------------------------

class App:

    def __init__(self, root):

        self.root = root
        self.root.title("NostalgiaHub - Sprint 2")
        self.root.geometry("520x540")

        self.service = ColeccionService()
        self.indice = None

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
        frame_cat.pack(fill="x", padx=10)

        self.entry_categoria = tk.Entry(frame_cat, width=30)
        self.entry_categoria.grid(row=0, column=0)

        tk.Button(
            frame_cat,
            text="Crear",
            command=self.crear_categoria
        ).grid(row=0, column=1)

        self.lista_categorias = tk.Listbox(frame_cat, height=5)
        self.lista_categorias.grid(row=1, column=0, columnspan=2, pady=10, sticky="we")

        self.lista_categorias.bind("<<ListboxSelect>>", self.seleccionar_categoria)

        # -----------------------------
        # AGREGAR / EDITAR ELEMENTO
        # -----------------------------

        frame_elem = tk.LabelFrame(root, text="Agregar / Editar Elemento", padx=10, pady=10)
        frame_elem.pack(fill="x", padx=10, pady=10)

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
            text="Agregar",
            command=self.agregar
        ).grid(row=4, column=0)

        tk.Button(
            frame_elem,
            text="Guardar cambios",
            command=self.editar
        ).grid(row=4, column=1)

        # -----------------------------
        # VER ELEMENTOS
        # -----------------------------

        frame_ver = tk.LabelFrame(root, text="Ver Elementos", padx=10, pady=10)
        frame_ver.pack(fill="both", expand=True, padx=10)

        tk.Label(frame_ver, text="Categoría").grid(row=0, column=0)

        self.cat_ver = tk.Entry(frame_ver)
        self.cat_ver.grid(row=0, column=1)

        tk.Button(
            frame_ver,
            text="Mostrar",
            command=self.ver
        ).grid(row=0, column=2)

        tk.Button(
            frame_ver,
            text="Editar seleccionado",
            command=self.cargar
        ).grid(row=0, column=3)

        self.lista = tk.Listbox(frame_ver, height=8)
        self.lista.grid(row=1, column=0, columnspan=4, pady=10, sticky="we")

        # limpiar lista si cambia categoría
        self.cat_ver.bind("<KeyRelease>", self.limpiar_lista)

    # -----------------------------
    # FUNCIONES
    # -----------------------------

    def crear_categoria(self):

        try:

            nombre = self.entry_categoria.get().strip()

            self.service.crear_categoria(nombre)

            self.entry_categoria.delete(0, tk.END)

            self.actualizar_lista()

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

        self.cat_ver.delete(0, tk.END)
        self.cat_ver.insert(0, categoria)

        self.lista.delete(0, tk.END)

    def agregar(self):

        try:

            self.service.agregar_elemento(
                self.cat.get(),
                self.nombre.get(),
                self.anio.get(),
                self.estado.get()
            )

            messagebox.showinfo("Éxito", "Elemento agregado")

            # limpiar campos
            self.cat.delete(0, tk.END)
            self.nombre.delete(0, tk.END)
            self.anio.delete(0, tk.END)
            self.estado.set("Bueno")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def ver(self):

        try:

            categoria = self.cat_ver.get()

            elementos = self.service.obtener_elementos(categoria)

            self.lista.delete(0, tk.END)

            if not elementos:
                messagebox.showinfo("Información", "No hay elementos en esta categoría")
                return

            for e in elementos:
                texto = f"{e.nombre} | Año: {e.anio} | Estado: {e.estado}"
                self.lista.insert(tk.END, texto)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cargar(self):

        seleccion = self.lista.curselection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un elemento")
            return

        indice = seleccion[0]

        categoria = self.cat_ver.get()

        elemento = self.service.obtener_elementos(categoria)[indice]

        self.indice = indice

        self.cat.delete(0, tk.END)
        self.cat.insert(0, categoria)

        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, elemento.nombre)

        self.anio.delete(0, tk.END)
        self.anio.insert(0, elemento.anio)

        self.estado.set(elemento.estado)

    def editar(self):

        if self.indice is None:
            messagebox.showwarning("Aviso", "Seleccione un elemento primero")
            return

        self.service.editar_elemento(
            self.cat.get(),
            self.indice,
            self.nombre.get(),
            self.anio.get(),
            self.estado.get()
        )

        messagebox.showinfo("Éxito", "Elemento actualizado")

        self.ver()

    def limpiar_lista(self, event):

        self.lista.delete(0, tk.END)


# -----------------------------
# MAIN
# -----------------------------

root = tk.Tk()
app = App(root)
root.mainloop()