"""
En el main vamos a llamar a cada una de nuestras funciones de manejo de datos utilizando un GUI como tkinter.
El flujo sería un Recolectar (datos de la interfaz) -> Ejecutar (funciones del handler) -> Avisar (resultado)


"""
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
import data_handler as dh

""" Primero vamos a crear 2 funciones que representan el puente entre la GUI y Pandas. Una que se centra en
actualizar la la lista de columnas en el Listbox cuando se carga un archivo y muestra el df actual. Como 
el listbox devuelve números cuando seleccionamos columnas, y nosotros tenemos las nuestras con str en el df
vamos a utilizar una función que recorre los números y busca el texto correspondiente en el df.
    """

def actualizar_listbox():
    listbox_columnas.delete(0, tk.END) # 1. Borrar todo, del 0 al end (último elemento)
    
    # Accedemos a la variable df dentro de data_handler
    if dh.df is not None:
        for col in dh.df.columns:
            listbox_columnas.insert(tk.END, col) # Mete las columnas en el listbox

def obtener_seleccion():
    indices = listbox_columnas.curselection() # Obtiene indices numéricos de las opciones seleccionadas
    nombres = []
    for i in indices:
        nombres.append(listbox_columnas.get(i)) # Trae el texto real almacenado en esa posición y lo asigna a nombres
    return nombres

def boton_cargar():
    # filedialog.askopenfilename() abre la ventana de selección de archivos
    ruta = filedialog.askopenfilename(filetypes=[("CSV o JSON", "*.csv *.json")])
    
    if ruta: #de esta manera si el usuria ingresa una str vacío o cancela es falso y no entra al if
        
        resultado = dh.cargar_archivo(ruta)
        
        if resultado is not None:
            lbl_archivo.config(text=f"Archivo: {ruta.split('/')[-1]}") # Mostramos solo el nombre
            actualizar_listbox() # Acá mostrar las columnas nuevas del archivo recien cargado
            messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo cargar el archivo.")
            
def boton_eliminar_nulls():
    columnas = obtener_seleccion()
    if not columnas:
        messagebox.showwarning("Atención", "Selecciona al menos una columna.")
        return
    
    dh.eliminar_nulls(columnas)
    messagebox.showinfo("Info", "Proceso de eliminación finalizado.")
    # Acá no hace falta actualizar el listbox porque las columnas siguen llamandose igual, solo se sacaron los nulls
    
def boton_rellenar_nulls():
    columnas = obtener_seleccion()
    valor = entry_relleno.get() # Definimos el valor a reemplazar
    
    if not columnas:
        messagebox.showwarning("Atención", "Selecciona columnas.")
        return
    if not valor:
        messagebox.showwarning("Atención", "Escribe un valor de relleno.")
        return

    dh.rellenar_nulls(columnas, valor)
    messagebox.showinfo("Info", "Relleno completado (revisa la consola por errores de tipo).")
    
def boton_duplicados():
    columnas = obtener_seleccion()
    # Como la fun acepta listas vacías para borrar en todo el df, no lo validamos con el if
    dh.eliminar_duplicados(columnas)
    messagebox.showinfo("Info", "Duplicados eliminados.")

def boton_texto(tipo):
    """Para simplificar las módificaciones de la fuente, vamos a crear una función generica
    para los 3 botones de texto (Lower, Upper, Capitalize)"""
    columnas = obtener_seleccion()
    if not columnas:
        messagebox.showwarning("Atención", "Selecciona columnas.")
        return

    if tipo == "minuscula":
        dh.minuscula(columnas)
    elif tipo == "mayuscula":
        dh.mayuscula(columnas)
    elif tipo == "capitalizar":
        dh.capitalizar(columnas)
        
    messagebox.showinfo("Info", f"Formato {tipo} aplicado.")

def boton_buscar_reemplazar():
    columnas = obtener_seleccion()
    valor_buscar = entry_buscar.get()
    valor_reemplazo = entry_reemplazar.get()
    
    if not columnas:
        messagebox.showwarning("Atención", "Selecciona columnas donde buscar.")
        return
    if not valor_buscar:
        messagebox.showwarning("Atención", "Escribe qué valor buscar.")
        return
    
    # Llamamos al handler
    dh.buscar_reemplazar(columnas, valor_buscar, valor_reemplazo)
    messagebox.showinfo("Info", "Reemplazo finalizado.")
    
def boton_exportar(formato):
    if dh.df is None:
        messagebox.showwarning("Error", "No hay datos para exportar.")
        return

    if formato == "csv":
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        """Con filedialog.asksaveasfilename abrimos el explorador de W, elegimos donde guardar el archivo y con que nombre
        """
        if ruta:    # solo si hay una ruta válida ahí llama a la fun del handler
            dh.to_csv(ruta)
            messagebox.showinfo("Éxito", "CSV Guardado.")
            
    elif formato == "json":
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if ruta:
            dh.to_json(ruta)
            messagebox.showinfo("Éxito", "JSON Guardado.")

""" A partir de acá es donde definimos cómo será nuestra interfaz de Tkinter. Desde los estético, hasta cómo
se distribuye. Esta librería, funciona con un sistema de contenedores donde cada ventana o sección se construye 
dentro de otra. El contenedor base de todo es tk() que es el root, y dentro de esto metemos frames que son como 
cajas donde llamamos a cada uno de los widgets de tkinter (.button, .label, .labelframe) 
"""
            
root = tk.Tk() #crea la ventana principal que se llamará root y definimos nombre y tamaño
root.title("PandasOS")
root.geometry("500x600")

# --- 1: CARGA DE ARCHIVO ---
# Carga del archivo, donde con label frame creamos el recuadro y el título, y luego con .pack gestionamos la ubicación
frame_carga = tk.LabelFrame(root, text=" 1. Cargar Datos ", padx=10, pady=10) 
frame_carga.pack(fill="x", padx=10, pady=5) 

#Aquí creamos con .button el boton para selec el archivo asignandole la función correspondiente y su color
btn_cargar = tk.Button(frame_carga, text="Seleccionar Archivo", command=boton_cargar, bg="#dddddd")
btn_cargar.pack(side=tk.LEFT)

#aca mostramos un label/texto que muestra que no hay archivo cargado pero que cambia dinámicamente al cargar el archivo
lbl_archivo = tk.Label(frame_carga, text="Ningún archivo cargado", fg="gray")
lbl_archivo.pack(side=tk.LEFT, padx=10)

# --- 2: SELECTOR DE COLUMNAS ---
frame_lista = tk.LabelFrame(root, text=" 2. Seleccionar Columnas ", padx=10, pady=10)
frame_lista.pack(fill="both", expand=True, padx=10, pady=5)

# Agragamos el Scrollbar de tk para lograr recorrer todo si hay muchas columnas
scrollbar = Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill="y")

"""Acá Listbox se coloca dentro del contenedor frame_lista, le pusimos el modo MULTIPLE porque permite seleccionar 
varias listas clickeando.
"""
listbox_columnas = tk.Listbox(frame_lista, selectmode=tk.MULTIPLE, height=6, yscrollcommand=scrollbar.set)
listbox_columnas.pack(fill="both", expand=True)
scrollbar.config(command=listbox_columnas.yview)

# --- 3: OPERACIONES  ---
frame_ops = tk.LabelFrame(root, text=" 3. Operaciones de Limpieza ", padx=10, pady=10)
frame_ops.pack(fill="x", padx=10, pady=5)

# Fila 1: Eliminar Nulos y Duplicados
btn_drop_nulls = tk.Button(frame_ops, text="Eliminar Nulos", command=boton_eliminar_nulls, bg="#ffcccc")
btn_drop_nulls.grid(row=0, column=0, padx=5, pady=5)

btn_drop_dupli = tk.Button(frame_ops, text="Eliminar Duplicados", command=boton_duplicados, bg="#ffcccc")
btn_drop_dupli.grid(row=0, column=1, padx=5, pady=5)

# Fila 2: Rellenar Nulos (Etiqueta + Entrada + Botón)
#Creamos una etiqueta que es "Reemplazar...", le ponemos una caja de texto para ingresar el valor y un boton para ejecutar
tk.Label(frame_ops, text="Reemplazar Nulls con:").grid(row=1, column=0, sticky="e")
entry_relleno = tk.Entry(frame_ops, width=15)
entry_relleno.grid(row=1, column=1, padx=5)
btn_fill_nulls = tk.Button(frame_ops, text="Aplicar", command=boton_rellenar_nulls, bg="#ffffcc")
btn_fill_nulls.grid(row=1, column=2, padx=5)

# --- 4: EDICIÓN DE TEXTO ---
frame_text = tk.LabelFrame(root, text=" 4. Formato de Texto ", padx=10, pady=10)
frame_text.pack(fill="x", padx=10, pady=5)

btn_lower = tk.Button(frame_text, text="Minúscula", command=lambda: boton_texto("minuscula"))
btn_lower.pack(side=tk.LEFT, padx=5, expand=True, fill="x")

btn_upper = tk.Button(frame_text, text="Mayúscula", command=lambda: boton_texto("mayuscula"))
btn_upper.pack(side=tk.LEFT, padx=5, expand=True, fill="x")

btn_cap = tk.Button(frame_text, text="Capitalizar", command=lambda: boton_texto("capitalizar"))
btn_cap.pack(side=tk.LEFT, padx=5, expand=True, fill="x")

# --- 5: BUSCAR Y REEMPLAZAR ---
frame_buscar_reemplazar = tk.LabelFrame(root, text=" 5. Buscar y Reemplazar ", padx=10, pady=10)
frame_buscar_reemplazar.pack(fill="x", padx=10, pady=5)


tk.Label(frame_buscar_reemplazar, text="Buscar:").grid(row=0, column=0, sticky="e")
entry_buscar = tk.Entry(frame_buscar_reemplazar, width=15)
entry_buscar.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_buscar_reemplazar, text="Reemplazar con:").grid(row=1, column=0, sticky="e")
entry_reemplazar = tk.Entry(frame_buscar_reemplazar, width=15)
entry_reemplazar.grid(row=1, column=1, padx=5, pady=2)

btn_replace = tk.Button(frame_buscar_reemplazar, text=" Aplicar", command=boton_buscar_reemplazar, bg="#ffeebb")
btn_replace.grid(row=0, column=2, rowspan=2, padx=15, ipady=5)

# --- 6: EXPORTAR ---
frame_export = tk.Frame(root, pady=10)
frame_export.pack(fill="x", padx=10)

boton_guardar_csv = tk.Button(frame_export, text="Guardar CSV", bg="#ccffcc", command=lambda: boton_exportar("csv"))
boton_guardar_csv.pack(side=tk.LEFT, expand=True, fill="x", padx=5)

boton_guardar_json = tk.Button(frame_export, text="Guardar JSON", bg="#ccffcc", command=lambda: boton_exportar("json"))
boton_guardar_json.pack(side=tk.LEFT, expand=True, fill="x", padx=5)

#Mantiene abierto la ventana (root) en un loop constante, si no se cerraría al instante.
root.mainloop()