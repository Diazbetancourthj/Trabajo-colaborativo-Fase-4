#Módulo: logger_config.py
# Descripción: Configuración centralizada del sistema de registro de eventos
#              y errores (logging) en archivo de texto para Software FJ.
# ==============================================================================

# Importa el módulo estándar de Python para el registro de eventos y trazabilidad
import logging
# Importa el módulo os para gestionar rutas de archivos del sistema operativo
import os


def configurar_logger(nombre_archivo: str = "sistema.log") -> logging.Logger:
    """Configura y devuelve el logger principal que registra eventos y errores en un archivo de logs."""
    # Obtiene la ruta absoluta del directorio donde se encuentra este script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Construye la ruta completa hacia el archivo de registro de eventos (sistema.log)
    ruta_log = os.path.join(directorio_actual, nombre_archivo)

    # Obtiene el logger raíz del sistema para centralizar todos los registros de los módulos
    logger_raiz = logging.getLogger()
    # Establece el nivel mínimo de captura en INFO para registrar tanto eventos como errores
    logger_raiz.setLevel(logging.INFO)

    # Verifica si el logger ya tiene manejadores configurados para evitar duplicación de líneas
    if not logger_raiz.handlers:
        # Define el formato detallado de cada línea del log: fecha/hora, nivel, módulo y mensaje
        formato_log = logging.Formatter(
            fmt="%(asctime)s | [%(levelname)s] | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Crea el manejador de archivo con codificación UTF-8 para soportar tildes y caracteres en español
        manejador_archivo = logging.FileHandler(ruta_log, mode="a", encoding="utf-8")
        # Establece el nivel INFO para que todos los eventos y errores queden guardados en el archivo
        manejador_archivo.setLevel(logging.INFO)
        # Asigna el formato definido al manejador de archivo
        manejador_archivo.setFormatter(formato_log)

        # Agrega el manejador de archivo al logger raíz del sistema
        logger_raiz.addHandler(manejador_archivo)

    # Registra un evento informativo indicando que el sistema de logs fue inicializado correctamente
    logging.info("Sistema de registro de logs (logger_config) inicializado correctamente.")
    # Retorna la instancia del logger configurado
    return logger_raiz

