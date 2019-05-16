import tkinter as tk

ventana = tk.Tk()

nombre = tk.StringVar()
tk.Entry(ventana, textvariable=nombre, width=30).grid(row=0, column=1)
tk.Label(ventana, text = 'Nombre').grid(row=0, column=0)

apellido = tk.StringVar()
tk.Entry(ventana, textvariable=apellido, width=30).grid(row=1, column=1)
tk.Label(ventana, text = 'Apellido').grid(row=1, column=0)

celular = tk.StringVar()
tk.Entry(ventana, textvariable=celular, width=30).grid(row=2, column=1)
tk.Label(ventana, text = 'Celular').grid(row=2, column=0)

contactos={}

def guardar():
    nom = nombre.get()
    cel = celular.get()
    contactos[nom] = cel

guardar_btn = tk.Button(ventana, text='Guardar', command = guardar)
guardar_btn.grid(row=3, column=0, columnspan=2, sticky = 'ew')

imprimir_btn = tk.Button(ventana, text='Guardar', command = lambda: print(contactos))
imprimir_btn.grid(row=4, column=0, columnspan=2, sticky = 'ew')

ventana.mainloop()
