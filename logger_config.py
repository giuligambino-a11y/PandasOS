import logging #módulo logging.
import os #módulo para movimientos en el OS.

#Crear carpeta 'data', y de existir no la crea.
LOG_DIR = "data"
os.makedirs(LOG_DIR, exist_ok=True)

# Define la ruta del log.
LOG_FILE = os.path.join(LOG_DIR, "registro.log")
# Creamos el logger pidiendoselo al módulo y marcamos en nivel default de log como el de info.
logger = logging.getLogger("PandasOS")
logger.setLevel(logging.INFO)

#Creamos un handler estableciendo como va a escribir en el log
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Formato del log
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# Evita agregar handlers duplicados
if not logger.handlers:
    logger.addHandler(file_handler)

# Desactivar propagación al logger raíz
logger.propagate = False

