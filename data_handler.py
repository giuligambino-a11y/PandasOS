"""
El objetivo de este módulo es contener toda la lógica de pandas que usaremos en nuestra GUI.

Funciones:
1-cargar_archivo
2-eliminar_nulls
3-rellenar_nulls
4-eliminar_duplicados
5-minúscula
6-mayúscula
7-capitalizar
8-to_csv
9-to_json

"""
import pandas as pd
from logger_config import logger


df = None

def cargar_archivo(path):
    """
    Esta es la función que cargar los archivos con los que trabajaremos. En un principio, solo se podrán usar
    json o csv. 
    
    """
    global df #nos permite modificar una variable por fuera de la función
    try:
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".json"):
            df = pd.read_json(path)
        else:
            logger.warning("Formato ingresado inválido.") 
            raise ValueError("Formato no soportado. Los formatos válidos son CSV o JSON.")
        
        logger.info("Archivo cargado exitosamente")    
        return df
    
    except FileNotFoundError:
        print(f"No se encontró el archivo: {path}")
        logger.error("El archivo no existe o la ruta es incorrecta.")
        
    except pd.errors.ParserError:
        # Esto pasa si el contenido está roto
        print(f"Archivo corrupto o mal formado: {path}")
        logger.error("El archivo parece estar dañado o tener un formato incorrecto.")

    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")
    
    return None
        
    
    
def eliminar_nulls(columnas_seleccionadas):
    
    """
    Esta es la función que va a eliminar los nulls de las columnas que nosotros le pidamos. Se espera que
    variable columnas_seleccionadas sea una lista (ej: ['Edad', 'Nombre']) 
    
    """
    global df

    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return

    
    try:
        
        df.dropna(subset=columnas_seleccionadas, inplace=True)
        """
        Subset permite que el dropna solo sea en las columnas especificadas y no en todo el dt.
        El inplace=True nos permite editar el archivo original, de esta manera no se crea una copia
        momentanea del df y se aplica el cambio guardándolo. 
        """
        print(f"Limpieza completada en las columnas: {columnas_seleccionadas}")
        logger.info ("Limpieza de nulls por columna completada")

    except KeyError as e:
        print(f"Error: La columna no existe - {e}")
        logger.warning("No se encontró la columna")
        
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")
        

def rellenar_nulls(columnas_seleccionadas,valor):
    """
    Esta es la función que va rellenar los nulls para las columnas especificadas con un valor especifico. 
    Previo a el relleno propiamente dicho, cabe aclarar que el Entry en Tkinter devuelve un str. Si tenemos una columna int
    y la rellenamos con un str podríamos convertirla toda en str complicando luego si queremos hacer operaciones algebráicas.
    Por lo que tenemos que añadir pequeña validación para detectar si el usuario escribió un número e intentar convertirlo 
    antes de rellenar. 
    
    """
    global df
    
    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return

    # Validamos/convertimos el valor mediante la lógica cascada de intentos
    valor_final = valor 
    es_numero = False # Bandera para saber si logramos convertirlo

    try:
        valor_final = int(valor)
        es_numero = True
    except ValueError:
        try:
            valor_final = float(valor)
            es_numero = True
        except ValueError:
            valor_final = valor
            es_numero = False # Es texto

    #Validamos la compatibilidad de tipo con su respectiva columna
    try:
        for columna in columnas_seleccionadas:
            # Obtenemos el tipo de dato de la columna actual
            tipo_columna = df[columna].dtype
            
            # Esta funcion de Panda verifica si la columna si es numero (int o float) y devuelve valor True o False
            columna_es_numerica = pd.api.types.is_numeric_dtype(tipo_columna)
            
            if columna_es_numerica and not es_numero:
                print(f"Error: La columna '{columna}' es numérica, no puedes rellenarla con el texto '{valor_final}'.")
                logger.warning(f"Intento de tipo inválido en columna")
                return  # Salimos de la función sin tocar nada
    
        df[columnas_seleccionadas] = df[columnas_seleccionadas].fillna(valor)
        """A diferencia de antes donde usabamos el inplace=True para que modifique el archivo original, acá
        debido a que fillna no permite elegir un subset donde vamos a rellenar los nulls tenemos que definir
        una variable especifica de columna dentro del df. Una vez definida decimos que a esa columna dentro del df 
        le reñllenemos los nulls con nuestro valor. Si ponemos el inplace=True ahí dentro puede que nos modifique la
        copia del df y no el original, por eso de esta forma, le decimos directamente que esa modificación es parte 
        del original df[col...] (original) = df[col..].fillna (modificación hecha)
        
        """
        
        print(f"Reemplazo completado en las columnas: {columnas_seleccionadas}")
        logger.info ("Remplazo nulls por columna completado")

    except KeyError as e:
        print(f"Error: La columna no existe - {e}")
        logger.warning("No se encontró la columna")
        
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")

def eliminar_duplicados(columnas_seleccionadas):
    """
    Esta es la función que va a eliminar los duplicados solo para las columnas seleccionadas, es decir, con ya 
    haber coincidencia en las filas de la/s columna/s seleccionadas borra el duplicado y se queda con el primero.
    Si el usuario quiere incluir todas las columnas, osea coincidencia total de filas, no tiene que meter un valor en 
    columnas_seleccionadas.
    
    """
    global df
    
    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return
    
    try:
        if not columnas_seleccionadas:
            df.drop_duplicates(keep="first",inplace=True)
        else:    
            df.drop_duplicates(subset=columnas_seleccionadas,keep="first",inplace=True)
            
        print("Duplicados eliminados correctamente")
        logger.info("Duplicados eliminados correctamente")
        
    except KeyError as e:
        print(f"Error: La columna no existe - {e}")
        logger.warning("No se encontró la columna")
        
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")
        
def minuscula(columnas_seleccionadas):
    """
    Esta es la función que va poner en minúsculas los valores de las columnas seleccionadas. A diferencia de dropna o 
    drop_duplicates, las funciones de texto en Pandas nunca tienen inplace=True. Así que tenemos que guardarla 
    manualmente sobrescribiendo la columna como hicimos en .fillna.
    
    """
    global df
    
    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return
    
    try:
        for columna in columnas_seleccionadas: #recorre columna por columna
            df[columna] = df[columna].astype(str).str.lower()
        
        print(f"Minúsculas aplicadas correctamente en {columnas_seleccionadas}")
        logger.info("Minúsculas aplicadas correctamente")        
        
    
    except KeyError as e:
        print(f"Error: La columna no existe - {e}")
        logger.warning("No se encontró la columna")
        
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")

def mayuscula(columnas_seleccionadas):
    """
    Esta es la función que va poner en Mayúsculas los valores de las columnas seleccionadas. 
    
    """
    global df
    
    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return
    
    try:
        for columna in columnas_seleccionadas: #recorre columna por columna
            df[columna] = df[columna].astype(str).str.upper()
        
        print(f"Mayúsculas aplicadas correctamente en {columnas_seleccionadas}")
        logger.info("Mayúsculas aplicadas correctamente")        
        
    
    except KeyError as e:
        print(f"Error: La columna no existe - {e}")
        logger.warning("No se encontró la columna")
        
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")
        
def capitalizar(columnas_seleccionadas):
    """
    Esta es la función que va poner en Mayúsculas la primera letra del valores. 
    
    """
    global df
    
    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return
    
    try:
        for columna in columnas_seleccionadas: #recorre columna por columna
            df[columna] = df[columna].astype(str).str.capitalize()
        
        print(f"Capitalización aplicada correctamente en {columnas_seleccionadas}")
        logger.info("Capitalización aplicada correctamente")        
        
    
    except KeyError as e:
        print(f"Error: La columna no existe - {e}")
        logger.warning("No se encontró la columna")
        
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")

def buscar_reemplazar(columnas_seleccionadas, valor_buscar, valor_reemplazar):
    """
    Busca un valor específico y lo reemplaza por otro en las columnas seleccionadas.
    Maneja la conversión de tipos (si buscas un número escrito como texto).
    """
    global df
    
    if df is None:
        logger.warning("Intento de búsqueda sin archivo cargado")
        return

    # Acá buscamos convertir los inputs a número ya que en entry de tk solo maneja str
    buscar_final = valor_buscar
    try:
        buscar_final = int(valor_buscar)
    except ValueError:
        try:
            buscar_final = float(valor_buscar)
        except ValueError:
            buscar_final = valor_buscar 

    # Acá hacemos lo mismo pero con el remplazo de str --> int
    reemplazo_final = valor_reemplazar
    try:
        reemplazo_final = int(valor_reemplazar)
    except ValueError:
        try:
            reemplazo_final = float(valor_reemplazar)
        except ValueError:
            reemplazo_final = valor_reemplazar

    try:
        for columna in columnas_seleccionadas:
            
            df[columna] = df[columna].replace(to_replace=buscar_final, value=reemplazo_final)
            #usando el .replace de pandas logramos el cometido
        
        print(f"Reemplazo de '{buscar_final}' por '{reemplazo_final}' aplicado en: {columnas_seleccionadas}")
        logger.info(f"Búsqueda y reemplazo completados en {columnas_seleccionadas}")

    except KeyError as e:
        print(f"Error: La columna no existe - {e}")
        logger.warning(f"No se encontró la columna: {e}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        logger.warning(f"Error al reemplazar: {e}")

def to_csv(path):
    """
    Esta es la función que va exportar en formato csv nuestro df. 
    
    """
    global df
    
    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return
    
    try:
        df.to_csv(path,encoding='utf-8-sig', index=False) #le decimos que el índex es falso así no lo incluye en el csv
        
        print("Guardado como .csv correctamente")
        logger.info("Guardado como .csv correctamente") 
    
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")
    
    return None

def to_json(path):
    """
    Esta es la función que va exportar en formato json nuestro df. 
    
    """
    global df
    
    if df is None:
        print("No hay ningún archivo cargado.")
        logger.warning("Archivo no encontrado") 
        return
    
    try:
        df.to_json(path,orient='records', force_ascii=False , indent=4)
        """Aquí le decimos que la orient='records' para que nos guarde formato lista de objetos.
        El force_ascii=False permite guardar tildes y ñ.
        """
        
        print("Guardado como .json correctamente")
        logger.info("Guardado como .json correctamente") 
    
    except Exception as e:
        # Atrapa cualquier otro error raro que no esperabas
        print(f"Error inesperado: {e}")
        logger.warning("Ocurrió un error inesperado")
    
    return None