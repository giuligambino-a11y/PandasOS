# PandasOS – GUI basada en Pandas

Este proyecto consiste en una aplicación de escritorio desarrollada en **Python**, utilizando **Tkinter** para la interfaz gráfica y **Pandas** para la manipulación de datos. Permite cargar archivos CSV o JSON, visualizar sus columnas y aplicar transformaciones básicas para limpieza de datos.

---

## Objetivo del proyecto

El objetivo del proyecto es brindar una solución fácil y sencilla para los usuarios que deseen limpiar y transformar conjuntos de datos. Herramientas potentes como Pandas suelen ser poco accesibles para el usuario no especializado, por lo que se quiso brindar una herramienta intuitiva e ilustrativa para ejecutar funciones básicas. 

---

## Funcionalidades principales

### Cargar datasets (CSV o JSON)
- Selección mediante ventana de archivos
- Visualización del nombre del archivo cargado
- Lectura automática mediante `pandas.read_csv()` o `pandas.read_json()`

### Listado de columnas del dataframe
- Listbox con selección múltiple
- Scrollbar integrado
- Actualización dinámica cuando se carga un nuevo archivo

### Operaciones de limpieza
- Relleno de valores nulos (`.fillna`)
- Conversión de texto a mayúsculas o minúsculas (`.upper`,`.lower`,`.capitalize`)
- Eliminación de filas nulas totales (`.dropna`)
- Eliminación de duplicados por columna (`.drop_duplicates`)
- Buscar y reemplazar (`.replace`)

---

## Arquitectura del proyecto

El proyecto se divide en dos grandes módulos:

###  `data_handler.py`
Contiene toda la lógica de transformación de datos con Pandas.  
Se encarga de:

- Cargar archivos  
- Manipular el DataFrame  
- Aplicar las transformaciones  
- Exportarlo


### `main.py`
Contiene la interfaz hecha con Tkinter (librería nativa de Python) y las funciones nexo con las lógica del `data_handler`.  
Se encarga de:

- Dibujar la ventana
- Crear frames, botones y entradas
- Interactuar con `data_handler`
- Mostrar mensajes al usuario

---

## Estructura del proyecto

```
PandasOS/
│── main.py
│── data_handler.py
│── requirements.txt
│── README.md
└── data/
    └── registro.log
```

---

### Entorno virtual (venv)

Este proyecto utiliza un entorno virtual para gestionar las dependencias.

Para crearlo:
python -m venv venv

Para activarlo:
- Windows: venv\Scripts\activate
- Linux/Mac: source venv/bin/activate

Para instalar las dependencias:
pip install -r requirements.txt


