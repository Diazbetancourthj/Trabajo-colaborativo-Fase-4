# Módulo: excepciones.py
# Descripción: Define la jerarquía de excepciones personalizadas para el
#              Sistema Integral de Gestión de Clientes, Servicios y Reservas
#              de la empresa Software FJ (Curso Programación 213023 - UNAD).
# ==============================================================================


class SoftwareFJError(Exception):
    """Clase base para todas las excepciones personalizadas del sistema Software FJ."""

    def __init__(self, mensaje: str = "Error general en el sistema Software FJ."):
        # Inicializa la clase base Exception con el mensaje descriptivo del error
        super().__init__(mensaje)
        # Almacena el mensaje de error como atributo accesible de la instancia
        self.mensaje = mensaje


class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos personales de un cliente no superan las validaciones."""

    def __init__(self, mensaje: str = "Los datos proporcionados para el cliente son inválidos."):
        # Llama al constructor de la superclase SoftwareFJError pasando el mensaje
        super().__init__(mensaje)


class ServicioInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando un servicio tiene parámetros inválidos o no está disponible."""

    def __init__(self, mensaje: str = "Los parámetros configurados para el servicio son inválidos."):
        # Llama al constructor de la superclase SoftwareFJError pasando el mensaje
        super().__init__(mensaje)


class CalculoCostoError(ServicioInvalidoError):
    """Excepción lanzada cuando ocurre una inconsistencia en el cálculo de costos, impuestos o descuentos."""

    def __init__(self, mensaje: str = "Error en el cálculo de costos del servicio."):
        # Llama al constructor de ServicioInvalidoError pasando el mensaje detallado
        super().__init__(mensaje)


class ServicioNoDisponibleError(ServicioInvalidoError):
    """Excepción lanzada cuando se intenta reservar o utilizar un servicio que no está disponible."""

    def __init__(self, mensaje: str = "El servicio solicitado no se encuentra disponible actualmente."):
        # Llama al constructor de ServicioInvalidoError pasando el mensaje de disponibilidad
        super().__init__(mensaje)


class ReservaError(SoftwareFJError):
    """Excepción lanzada cuando ocurre un fallo durante la creación, confirmación o cancelación de una reserva."""

    def __init__(self, mensaje: str = "No fue posible procesar la operación sobre la reserva."):
        # Llama al constructor de la superclase SoftwareFJError pasando el mensaje
        super().__init__(mensaje)


class OperacionNoPermitidaError(ReservaError):
    """Excepción lanzada cuando se intenta realizar una transición de estado no permitida en una reserva."""

    def __init__(self, mensaje: str = "La operación solicitada no está permitida en el estado actual."):
        # Llama al constructor de ReservaError pasando el mensaje correspondiente
        super().__init__(mensaje)

