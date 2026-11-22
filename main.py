import logging
from logger_config import configurar_logger
from simulacion import ejecutar_simulacion


def main():
    configurar_logger()
    logging.info("Inicio del programa de Software FJ")
    print("Sistema de gestión de clientes, servicios y reservas - Software FJ")

    try:
        ejecutar_simulacion()
    except Exception as error:
        # Si algo falla sin controlar, se guarda en el log y el programa no se cae
        logging.error("Error inesperado en el programa: " + str(error))
        print("Ocurrió un error inesperado, revise el archivo de logs")
    else:
        logging.info("Las simulaciones terminaron correctamente")
    finally:
        logging.info("Fin del programa")
        print("Programa finalizado")


if __name__ == "__main__":
    main()
