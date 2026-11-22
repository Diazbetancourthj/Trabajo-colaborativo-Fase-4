 Módulo: reserva.py
# Descripción: Define la clase Reserva que integra Cliente, Servicio, duración
#              y estado, gestionando la confirmación, cancelación y procesamiento
#              con manejo avanzado y encadenamiento de excepciones.
# ==============================================================================

# Importa os y sys para asegurar la resolución de módulos locales en cualquier entorno o IDE
import os
import sys

# Inserta el directorio del archivo actual en sys.path
if "__file__" in globals():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa el módulo logging para registrar eventos y errores de las reservas en sistema.log
import logging
# Importa la clase Cliente y la clase abstracta EntidadSistema desde el módulo cliente
from cliente import Cliente, EntidadSistema
# Importa la clase abstracta Servicio desde el módulo servicio
from servicio import Servicio
# Importa las excepciones personalizadas necesarias para la gestión de reservas
from excepciones import (
    ReservaError,
    OperacionNoPermitidaError,
    ClienteInvalidoError,
    ServicioInvalidoError,
)


class Reserva(EntidadSistema):
    """Clase que gestiona el ciclo de vida de una reserva en el sistema Software FJ."""

    # Atributo de clase que actúa como secuenciador automático de identificadores de reserva
    contador = 1000

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: int = 1):
        """Inicializa una reserva integrando cliente, servicio, duración y estado inicial."""
        # Incrementa el contador global de reservas en una unidad
        Reserva.contador += 1
        # Genera el identificador único de la reserva con el prefijo RES-
        self.id_reserva = f"RES-{Reserva.contador}"
        # Asigna la instancia del cliente asociado a la reserva
        self.cliente = cliente
        # Asigna la instancia del servicio especializado solicitado
        self.servicio = servicio
        # Almacena la duración solicitada (horas, días o sesiones según el tipo de servicio)
        self.duracion = duracion
        # Establece el estado inicial de la reserva como 'Pendiente'
        self.estado = "Pendiente"
        # Inicializa el costo final de la reserva en cero hasta que sea procesada
        self.costo_final = 0.0
        # Registra en el archivo de logs la creación de la nueva reserva en estado Pendiente
        logging.info(f"Reserva creada [{self.id_reserva}] en estado '{self.estado}'.")

    def confirmar(self, *args, **kwargs) -> float:
        """Confirma la reserva delegando la validación y cálculo al método procesar()."""
        # Invoca al método procesar reenviando todos los argumentos posicionales y nombrados
        return self.procesar(*args, **kwargs)

    def cancelar(self) -> None:
        """Cancela una reserva confirmada empleando manejo de excepciones con try/except/finally."""
        # Inicia bloque try/except/finally para controlar intentos de cancelación no permitidos
        try:
            # Verifica que la reserva se encuentre actualmente en estado 'Confirmada'
            if self.estado != "Confirmada":
                # Lanza OperacionNoPermitidaError si se intenta cancelar una reserva no confirmada
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar la reserva {self.id_reserva} porque su estado actual es '{self.estado}'."
                )
            # Cambia el estado de la reserva a 'Cancelada'
            self.estado = "Cancelada"
            # Registra la cancelación exitosa en el archivo de logs
            logging.info(f"Reserva {self.id_reserva} cancelada exitosamente.")
            # Muestra en consola la confirmación de anulación de la reserva
            print(f" [CANCELADA] Reserva {self.id_reserva} anulada correctamente.")
        except OperacionNoPermitidaError as e:
            # Registra en el archivo de logs la advertencia/error por operación no permitida
            logging.error(f"Operación no permitida al cancelar {self.id_reserva}: {e}")
            # Informa por consola que la cancelación fue rechazada de manera controlada
            print(f" [AVISO] {e}")
            # Relanza la excepción encadenada dentro de ReservaError para quien desee capturarla
            raise ReservaError(f"Fallo al cancelar {self.id_reserva}: {e}") from e
        finally:
            # Bloque finally que se ejecuta siempre al terminar el intento de cancelación
            logging.info(
                f"Finalizó intento de cancelación para {self.id_reserva}. Estado actual: {self.estado}."
            )

    def procesar(self, *args, **kwargs) -> float:
        """
        Procesa la reserva validando cliente y servicio, calculando el costo polimórfico
        y empleando try/except/else/finally con encadenamiento de excepciones.
        """
        # Inicia bloque try/except/else/finally para procesar la reserva de forma segura
        try:
            # Registra en el archivo de logs el inicio del procesamiento de la reserva
            logging.info(f"Procesando reserva {self.id_reserva}...")
            # Verifica que el objeto cliente sea efectivamente una instancia válida de Cliente
            if not isinstance(self.cliente, Cliente):
                # Lanza ClienteInvalidoError si no se proporcionó un objeto Cliente válido
                raise ClienteInvalidoError("El cliente asociado a la reserva no es una instancia válida.")
            # Verifica que el objeto servicio sea efectivamente una instancia válida de Servicio
            if not isinstance(self.servicio, Servicio):
                # Lanza ServicioInvalidoError si no se proporcionó un objeto Servicio válido
                raise ServicioInvalidoError("El servicio asociado a la reserva no es una instancia válida.")

            # Ejecuta las validaciones internas del documento del cliente y parámetros del servicio
            if not self.cliente.validar_documento() or not self.servicio.validar_parametros():
                # Lanza ReservaError si alguna validación retorna False
                raise ReservaError("Datos inválidos detectados en el cliente o en el servicio.")

            # Si se pasó la duración como primer argumento posicional, actualiza el atributo duracion
            if len(args) > 0 and isinstance(args[0], (int, float)):
                # Actualiza la duración de la reserva con el valor recibido en args[0]
                self.duracion = args[0]
            # Si no se enviaron argumentos posicionales ni duración en kwargs, usa self.duracion
            elif len(args) == 0 and not any(k in kwargs for k in ("horas", "dias", "sesiones")):
                # Empaqueta self.duracion como primer argumento posicional para calcular_costo
                args = (self.duracion,)

            # Calcula el costo final llamando polimórficamente a calcular_costo del servicio
            self.costo_final = self.servicio.calcular_costo(*args, **kwargs)
            # Actualiza el estado de la reserva a 'Confirmada' tras superar todas las validaciones
            self.estado = "Confirmada"
        except (ClienteInvalidoError, ServicioInvalidoError, ValueError) as e:
            # Cambia el estado de la reserva a 'Fallida' ante errores de validación o cálculo
            self.estado = "Fallida"
            # Registra el error específico en el archivo de logs del sistema
            logging.error(f"Error en procesamiento de {self.id_reserva}: {e}")
            # Encadena la excepción original (from e) lanzando ReservaError
            raise ReservaError(f"Fallo en reserva {self.id_reserva}: {e}") from e
        except Exception as e:
            # Cambia el estado de la reserva a 'Fallida' ante cualquier error inesperado
            self.estado = "Fallida"
            # Registra el error crítico inesperado en el archivo de logs
            logging.error(f"Error crítico inesperado en {self.id_reserva}: {e}")
            # Encadena la excepción desconocida dentro de ReservaError
            raise ReservaError(f"Error inesperado al procesar {self.id_reserva}: {e}") from e
        else:
            # Bloque else: se ejecuta únicamente cuando el bloque try finaliza sin excepciones
            logging.info(
                f"Reserva {self.id_reserva} confirmada exitosamente. Costo total: ${self.costo_final:.2f}"
            )
            # Imprime en consola el mensaje de éxito con el costo total calculado
            print(f" [ÉXITO] {self.id_reserva} confirmada. Total: ${self.costo_final:.2f}")
            # Retorna el costo final calculado de la reserva
            return self.costo_final
        finally:
            # Bloque finally: se ejecuta siempre, haya ocurrido o no una excepción
            print(f" [ESTADO] Fin de intento para {self.id_reserva}. Estado: {self.estado}\n")

    def mostrar_reserva(self) -> str:
        """Retorna una cadena descriptiva con el resumen completo del estado de la reserva."""
        # Obtiene el nombre del cliente de manera segura si la instancia es válida
        nombre_cli = self.cliente.get_nombre() if isinstance(self.cliente, Cliente) else "Cliente Inválido"
        # Obtiene la descripción del servicio de manera segura si la instancia es válida
        desc_serv = self.servicio.describir() if isinstance(self.servicio, Servicio) else "Servicio Inválido"
        # Devuelve el resumen formateado con ID, cliente, servicio, duración, estado y costo
        return (
            f"Reserva [{self.id_reserva}] | Cliente: {nombre_cli} | "
            f"Servicio: {desc_serv} | Duración: {self.duracion} | "
            f"Estado: {self.estado} | Total: ${self.costo_final:.2f}"
        )

    def mostrar_datos(self) -> str:
        """Implementa el método abstracto de EntidadSistema delegando en mostrar_reserva()."""
        # Retorna la representación textual generada por mostrar_reserva()
        return self.mostrar_reserva()


# Permite probar reserva.py directamente al darle 'Run' en Visual Studio Code
if __name__ == "__main__":
    from servicio import ReservaSala
    print("=== PRUEBA DIRECTA DE RESERVA.PY ===")
    cli_demo = Cliente("Laura Gómez", "1098765432", "laura.gomez@empresa.com")
    sala_demo = ReservaSala("SALA-101", "Auditorio Principal", 120.0, 50)
    res_demo = Reserva(cli_demo, sala_demo, duracion=3)
    res_demo.confirmar(3, incluir_proyector=True)
    print(" ->", res_demo.mostrar_reserva())
    print("=== PRUEBA DIRECTA DE RESERVA.PY FINALIZADA SIN ERRORES ===")
