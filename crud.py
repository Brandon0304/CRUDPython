import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO


def conectar_bd():
    return mysql.connector.connect(user='root', password='', database='prueba')


# Crear ventana principal
root = tk.Tk()
root.title("Gestión de Contactos")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

font_title = ("Arial", 14, "bold")
font_text = ("Arial", 11)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

frame_insertar = ttk.Frame(notebook)
frame_editar = ttk.Frame(notebook)
frame_eliminar = ttk.Frame(notebook)
frame_mostrar = ttk.Frame(notebook)

notebook.add(frame_insertar, text="Insertar")
notebook.add(frame_editar, text="Editar")
notebook.add(frame_eliminar, text="Eliminar")
notebook.add(frame_mostrar, text="Mostrar")


def ejecutar_consulta(consulta, parametros=()):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    conexion.commit()
    cursor.close()
    conexion.close()


def insertar_contacto():
    def guardar():
        dni, nombre, apellido = entry_dni.get(), entry_nombre.get(), entry_apellido.get()
        if dni and nombre and apellido:
            ejecutar_consulta("INSERT INTO clientes (dni, nombre, apellido) VALUES (%s, %s, %s)",
                              (dni, nombre, apellido))
            messagebox.showinfo("Éxito", "Contacto insertado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    ttk.Label(frame_insertar, text="DNI:", font=font_text).pack()
    entry_dni = ttk.Entry(frame_insertar)
    entry_dni.pack()
    ttk.Label(frame_insertar, text="Nombre:", font=font_text).pack()
    entry_nombre = ttk.Entry(frame_insertar)
    entry_nombre.pack()
    ttk.Label(frame_insertar, text="Apellido:", font=font_text).pack()
    entry_apellido = ttk.Entry(frame_insertar)
    entry_apellido.pack()
    ttk.Button(frame_insertar, text="Guardar", command=guardar).pack(pady=10)


def mostrar_contactos():
    for widget in frame_mostrar.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(frame_mostrar, columns=("ID", "DNI", "Nombre", "Apellido"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("DNI", text="DNI")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.pack(fill=tk.BOTH, expand=True)

    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    cursor.close()
    conexion.close()


def editar_contacto():
    def actualizar():
        id_contacto, nombre, apellido = entry_id.get(), entry_nombre.get(), entry_apellido.get()
        if id_contacto and nombre and apellido:
            ejecutar_consulta("UPDATE clientes SET nombre = %s, apellido = %s WHERE id = %s",
                              (nombre, apellido, id_contacto))
            messagebox.showinfo("Éxito", "Contacto actualizado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    ttk.Label(frame_editar, text="ID del Contacto:", font=font_text).pack()
    entry_id = ttk.Entry(frame_editar)
    entry_id.pack()
    ttk.Label(frame_editar, text="Nuevo Nombre:", font=font_text).pack()
    entry_nombre = ttk.Entry(frame_editar)
    entry_nombre.pack()
    ttk.Label(frame_editar, text="Nuevo Apellido:", font=font_text).pack()
    entry_apellido = ttk.Entry(frame_editar)
    entry_apellido.pack()
    ttk.Button(frame_editar, text="Actualizar", command=actualizar).pack(pady=10)


def eliminar_contacto():
    def borrar():
        id_contacto = entry_id.get()
        if id_contacto:
            ejecutar_consulta("DELETE FROM clientes WHERE id = %s", (id_contacto,))
            messagebox.showinfo("Éxito", "Contacto eliminado correctamente")
        else:
            messagebox.showerror("Error", "Debe ingresar un ID")

    ttk.Label(frame_eliminar, text="ID del Contacto a Eliminar:", font=font_text).pack()
    entry_id = ttk.Entry(frame_eliminar)
    entry_id.pack()
    ttk.Button(frame_eliminar, text="Eliminar", command=borrar).pack(pady=10)


insertar_contacto()
editar_contacto()
eliminar_contacto()
mostrar_contactos()

root.mainloop()
