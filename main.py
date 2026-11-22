# Se importan las funciones del logger (archivo logger_config.py)
from logger_config import configurar_logger, registrar_evento, registrar_error

# Se importa la función que ejecuta las 10 simulaciones (archivo simulacion.py)
from simulacion import ejecutar_simulaciones

# Función principal del programa
def main():
    # Se prepara el archivo de logs donde se guardan eventos y errores
    configurar_logger()

    # Se registra que el programa empezó
    registrar_evento("Inicio del programa de Software FJ")
    print("Sistema de gestión de clientes, servicios y reservas - Software FJ")

    # Bloque try: aquí se intenta ejecutar las simulaciones
    try:
        ejecutar_simulaciones()

    # Bloque except: se ejecuta si ocurre un error que no se controló antes
    except Exception as error:
        # Se guarda el error en el log y el programa no se cae
        registrar_error("Error inesperado en el programa: " + str(error))
        print("Ocurrió un error inesperado, revise el archivo de logs")

    # Bloque else: se ejecuta solo si no hubo ningún error en el try
    else:
        registrar_evento("Las simulaciones terminaron correctamente")

    # Bloque finally: se ejecuta siempre, haya error o no
    finally:
        registrar_evento("Fin del programa")
        print("Programa finalizado")


# Esta condición hace que main() se ejecute solo cuando se corre este archivo
if __name__ == "__main__":
    main()
