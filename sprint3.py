from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# -----------------------------
# DATA
# -----------------------------

@dataclass
class Elemento:
    nombre: str
    anio: str
    estado: str


# -----------------------------
# LOGIC
# -----------------------------

class ColeccionService:

    def __init__(self):
        self.colecciones = {}

    def crear_categoria(self, nombre):

        if not nombre:
            raise ValueError("Ingrese un nombre")

        if nombre in self.colecciones:
            raise ValueError("La categoría ya existe")

        self.colecciones[nombre] = []

    def eliminar_categoria(self, categoria):
        del self.colecciones[categoria]

    def obtener_categorias(self):
        return list(self.colecciones.keys())

    def agregar_elemento(self, categoria, nombre, anio, estado):

        if not anio.isdigit():
            raise ValueError("El año debe ser numérico")

        self.colecciones[categoria].append(Elemento(nombre, anio, estado))

    def obtener_elementos(self, categoria):
        return self.colecciones[categoria]

    def editar_elemento(self, categoria, indice, nombre, anio, estado):

        if not anio.isdigit():
            raise ValueError("El año debe ser numérico")

        self.colecciones[categoria][indice] = Elemento(nombre, anio, estado)

    def eliminar_elemento(self, categoria, indice):
        del self.colecciones[categoria][indice]

    def contar_elementos(self, categoria):
        return len(self.colecciones[categoria])

    def buscar_elemento(self, nombre):

        resultados = []

        for categoria, elementos in self.colecciones.items():
            for e in elementos:
                if nombre.lower() in e.nombre.lower():
                    resultados.append((categoria, e))

        return resultados


# -----------------------------
# GUI
# -----------------------------

class App:

    def __init__(self, root):

        self.root = root
        self.root.title("NostalgiaHub - Sprint 3")
        self.root.geometry("760x520")

        self.service = ColeccionService()
        self.indice = None

        titulo = tk.Label(root,
                          text="Gestión de Colecciones Nostálgicas",
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        main = tk.Frame(root)
        main.pack(padx=10, pady=10)

        # COLUMNAS
        left = tk.Frame(main)
        left.grid(row=0, column=0, padx=10)

        right = tk.Frame(main)
        right.grid(row=0, column=1, padx=10)

        # -----------------------------
        # CATEGORIAS
        # -----------------------------

        frame_cat = tk.LabelFrame(left, text="Categorías", padx=10, pady=10)
        frame_cat.pack()

        self.entry_categoria = tk.Entry(frame_cat, width=20)
        self.entry_categoria.grid(row=0, column=0)

        tk.Button(frame_cat, text="Crear", command=self.crear_categoria).grid(row=0, column=1)
        tk.Button(frame_cat, text="Eliminar", command=self.eliminar_categoria).grid(row=0, column=2)

        self.lista_categorias = tk.Listbox(frame_cat, height=6, width=25)
        self.lista_categorias.grid(row=1, column=0, columnspan=3)

        self.lista_categorias.bind("<<ListboxSelect>>", self.seleccionar_categoria)

        # -----------------------------
        # ELEMENTOS
        # -----------------------------

        frame_elem = tk.LabelFrame(left, text="Elementos", padx=10, pady=10)
        frame_elem.pack(pady=15)

        tk.Label(frame_elem, text="Categoría").grid(row=0, column=0)

        self.cat_ver = tk.Entry(frame_elem)
        self.cat_ver.grid(row=0, column=1)

        tk.Button(frame_elem, text="Mostrar", command=self.ver).grid(row=0, column=2)
        tk.Button(frame_elem, text="Editar", command=self.cargar).grid(row=0, column=3)
        tk.Button(frame_elem, text="Eliminar", command=self.eliminar_elemento).grid(row=0, column=4)

        self.lista = tk.Listbox(frame_elem, width=45, height=10)
        self.lista.grid(row=1, column=0, columnspan=5, pady=10)

        # -----------------------------
        # AGREGAR / EDITAR
        # -----------------------------

        frame_add = tk.LabelFrame(right, text="Agregar / Editar Elemento", padx=10, pady=10)
        frame_add.pack()

        tk.Label(frame_add, text="Categoría").grid(row=0, column=0)
        self.cat = tk.Entry(frame_add)
        self.cat.grid(row=0, column=1)

        tk.Label(frame_add, text="Nombre").grid(row=1, column=0)
        self.nombre = tk.Entry(frame_add)
        self.nombre.grid(row=1, column=1)

        tk.Label(frame_add, text="Año").grid(row=2, column=0)
        self.anio = tk.Entry(frame_add)
        self.anio.grid(row=2, column=1)

        tk.Label(frame_add, text="Estado").grid(row=3, column=0)

        self.estado = ttk.Combobox(
            frame_add,
            values=["Excelente", "Bueno", "Regular", "Deteriorado"],
            state="readonly"
        )
        self.estado.grid(row=3, column=1)
        self.estado.set("Bueno")

        tk.Button(frame_add, text="Agregar", command=self.agregar).grid(row=4, column=0)
        tk.Button(frame_add, text="Guardar cambios", command=self.editar).grid(row=4, column=1)

        # -----------------------------
        # BUSCAR + CONTAR
        # -----------------------------

        frame_buscar = tk.LabelFrame(right, text="Buscar / Contar", padx=10, pady=10)
        frame_buscar.pack(pady=20)

        self.buscar_nombre = tk.Entry(frame_buscar)
        self.buscar_nombre.grid(row=0, column=0)

        tk.Button(frame_buscar, text="Buscar", command=self.buscar).grid(row=0, column=1)

        tk.Button(frame_buscar, text="Contar elementos", command=self.contar).grid(row=1, column=0, columnspan=2, pady=10)

    # -----------------------------
    # FUNCIONES
    # -----------------------------

    def crear_categoria(self):

        try:
            nombre = self.entry_categoria.get()
            self.service.crear_categoria(nombre)

            self.entry_categoria.delete(0, tk.END)

            self.actualizar_lista()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_categoria(self):

        seleccion = self.lista_categorias.curselection()

        if not seleccion:
            return

        categoria = self.lista_categorias.get(seleccion)

        if messagebox.askyesno("Confirmar", "¿Eliminar categoría?"):
            self.service.eliminar_categoria(categoria)
            self.actualizar_lista()

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

    def ver(self):

        categoria = self.cat_ver.get()

        elementos = self.service.obtener_elementos(categoria)

        self.lista.delete(0, tk.END)

        for e in elementos:
            self.lista.insert(tk.END, f"{e.nombre} | {e.anio} | {e.estado}")

    def cargar(self):

        seleccion = self.lista.curselection()

        if not seleccion:
            return

        indice = seleccion[0]

        categoria = self.cat_ver.get()

        elemento = self.service.obtener_elementos(categoria)[indice]

        self.indice = indice

        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, elemento.nombre)

        self.anio.delete(0, tk.END)
        self.anio.insert(0, elemento.anio)

        self.estado.set(elemento.estado)

    def editar(self):

        self.service.editar_elemento(
            self.cat.get(),
            self.indice,
            self.nombre.get(),
            self.anio.get(),
            self.estado.get()
        )

        self.ver()

    def eliminar_elemento(self):

        seleccion = self.lista.curselection()

        if not seleccion:
            return

        indice = seleccion[0]

        categoria = self.cat_ver.get()

        if messagebox.askyesno("Confirmar", "¿Eliminar elemento?"):
            self.service.eliminar_elemento(categoria, indice)
            self.ver()

    def buscar(self):

        nombre = self.buscar_nombre.get()

        resultados = self.service.buscar_elemento(nombre)

        self.lista.delete(0, tk.END)

        for categoria, e in resultados:
            self.lista.insert(tk.END, f"{categoria} -> {e.nombre} | {e.anio} | {e.estado}")

    def contar(self):

        categoria = self.cat_ver.get()

        cantidad = self.service.contar_elementos(categoria)

        messagebox.showinfo("Cantidad", f"{cantidad} elementos")


root = tk.Tk()
app = App(root)
root.mainloop()