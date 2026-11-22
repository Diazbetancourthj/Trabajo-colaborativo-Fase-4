from abc import ABC, abstractmethod
from excepciones import ServicioInvalidoError

class Servicio(ABC):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float):
        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        pass

    @abstractmethod
    def describir(self) -> str:
        pass

    def validar_parametros(self) -> bool:
        if self.costo_base < 0:
            raise ServicioInvalidoError("El costo base no puede ser negativo.")
        return True

# ReservaSala (Integrante 2)
class ReservaSala(Servicio):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, capacidad: int):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas: int, incluir_proyector: bool = False) -> float:
        if horas <= 0:
            raise ValueError("Las horas deben ser mayores a 0.")
        total = self.costo_base * horas
        if incluir_proyector:
            total += 50.0
        return total

    def describir(self) -> str:
        return f"Sala: {self.nombre_servicio} (Capacidad: {self.capacidad})"

# AlquilerEquipo (Integrante 3)
class AlquilerEquipo(Servicio):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, tipo_hardware: str):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.tipo_hardware = tipo_hardware

    def calcular_costo(self, dias: int, seguro_danos: bool = False) -> float:
        if dias <= 0:
            raise ValueError("Los días deben ser mayores a 0.")
        total = self.costo_base * dias
        if seguro_danos:
            total += 30.0 * dias
        return total

    def describir(self) -> str:
        return f"Equipo: {self.nombre_servicio} ({self.tipo_hardware})"

# AsesoriaEspecializada (Integrante 4 - Tu aporte)
class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, especialidad: str):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.especialidad = especialidad

    def calcular_costo(self, sesiones: int, nivel_senior: bool = False) -> float:
        if sesiones <= 0:
            raise ValueError("Las sesiones deben ser mayores a 0.")
        mult = 1.5 if nivel_senior else 1.0
        return (self.costo_base * sesiones) * mult

    def describir(self) -> str:
        return f"Asesoría: {self.nombre_servicio} ({self.especialidad})"




Clase AlquilerEquipo (Responsable: Integrante 3)
# ==============================================================================

class AlquilerEquipo(Servicio):
    """
    Clase derivada que representa el servicio de alquiler de equipos de cómputo
    y hardware especializado en Software FJ (Responsable: Integrante 3).
    """

    def __init__(
        self,
        codigo: str,
        nombre_servicio: str,
        costo_base: float,
        tipo_hardware: str,
        disponible: bool = True,
    ):
        """Inicializa el servicio de AlquilerEquipo validando el tipo de hardware y datos base."""
        # Almacena la categoría o especificación del hardware antes de la validación
        self.tipo_hardware = tipo_hardware
        # Invoca al constructor de la superclase Servicio
        super().__init__(codigo, nombre_servicio, costo_base, disponible)

    def validar_parametros(self) -> bool:
        """Método sobrescrito que valida los datos base y el tipo de hardware del equipo."""
        # Ejecuta las validaciones generales definidas en la superclase Servicio
        super().validar_parametros()
        # Verifica que el tipo de hardware sea una cadena no vacía
        if not isinstance(self.tipo_hardware, str) or not self.tipo_hardware.strip():
            # Construye el mensaje de error para tipo de hardware inválido
            mensaje = (
                f"Tipo de hardware inválido en equipo '{self.nombre_servicio}': "
                f"debe especificar una categoría válida."
            )
            # Registra el error en el archivo de logs
            logging.error(mensaje)
            # Lanza la excepción personalizada ServicioInvalidoError
            raise ServicioInvalidoError(mensaje)
        # Retorna True si la validación fue exitosa
        return True

    def calcular_costo(
        self,
        dias: int = 1,
        seguro_danos: bool = False,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        """
        Método sobrescrito y sobrecargado para calcular el costo de alquiler de un equipo
        por días, incluyendo opcionalmente seguro contra daños, impuestos y descuentos.
        """
        # Inicia bloque try/except/else/finally para capturar cualquier error de cálculo
        try:
            # Verifica la validez de los parámetros del servicio
            self.validar_parametros()
            # Comprueba que el número de días de alquiler sea mayor a 0
            if isinstance(dias, bool) or not isinstance(dias, (int, float)) or dias <= 0:
                # Lanza ValueError cuando los días son menores o iguales a cero
                raise ValueError("Los días de alquiler deben ser mayores a 0.")

            # Calcula el subtotal multiplicando el costo base diario por los días solicitados
            subtotal = float(self.costo_base) * float(dias)
            # Verifica si el cliente incluyó la póliza de seguro contra daños ($30 por día)
            if seguro_danos:
                # Adiciona el valor del seguro por cada día de alquiler
                subtotal += 30.0 * float(dias)

            # Aplica porcentajes opcionales de descuento e impuesto sobre el subtotal
            total = self.aplicar_impuestos_y_descuentos(subtotal, impuesto, descuento)
        except (ValueError, TypeError) as e:
            # Registra el error en el archivo de logs
            logging.error(f"Error al calcular costo en AlquilerEquipo [{self.codigo}]: {e}")
            # Encadena la excepción original dentro de CalculoCostoError
            raise CalculoCostoError(
                f"Cálculo inconsistente en AlquilerEquipo '{self.nombre_servicio}': {e}"
            ) from e
        else:
            # Registra el cálculo exitoso en el archivo de logs
            logging.info(
                f"Costo calculado en AlquilerEquipo [{self.codigo}]: dias={dias}, "
                f"seguro={seguro_danos}, desc={descuento}%, imp={impuesto}% -> Total=${total:.2f}"
            )
            # Retorna el monto total calculado
            return total
        finally:
            # Deja constancia de finalización en el log de depuración
            logging.debug(f"Finalizó ejecución de calcular_costo para AlquilerEquipo [{self.codigo}].")

    def describir(self) -> str:
        """Método sobrescrito que retorna la descripción del equipo en alquiler (Polimorfismo)."""
        # Devuelve una cadena formateada con los detalles del equipo y su tarifa diaria
        return (
            f"Equipo [{self.codigo}]: {self.nombre_servicio} "
            f"(Hardware: {self.tipo_hardware} | Tarifa: ${self.costo_base:.2f}/día)"
        )


# ==============================================================================
# Clase AsesoriaEspecializada (Responsable: Integrante 4)
# ==============================================================================

class AsesoriaEspecializada(Servicio):
    """
    Clase derivada que representa el servicio de consultoría y asesoría técnica
    especializada en Software FJ (Responsable: Integrante 4).
    """

    def __init__(
        self,
        codigo: str,
        nombre_servicio: str,
        costo_base: float,
        especialidad: str,
        disponible: bool = True,
    ):
        """Inicializa el servicio de AsesoriaEspecializada validando su especialidad."""
        # Almacena el área de especialidad técnica de la asesoría
        self.especialidad = especialidad
        # Invoca al constructor de la superclase Servicio
        super().__init__(codigo, nombre_servicio, costo_base, disponible)

    def validar_parametros(self) -> bool:
        """Método sobrescrito que valida los atributos base y la especialidad de la asesoría."""
        # Ejecuta las validaciones base de la superclase Servicio
        super().validar_parametros()
        # Verifica que la especialidad sea una cadena de texto no vacía
        if not isinstance(self.especialidad, str) or not self.especialidad.strip():
            # Construye el mensaje descriptivo de error
            mensaje = (
                f"Especialidad inválida en asesoría '{self.nombre_servicio}': "
                f"debe indicar un área de especialidad."
            )
            # Registra el error en el archivo de logs
            logging.error(mensaje)
            # Lanza la excepción personalizada ServicioInvalidoError
            raise ServicioInvalidoError(mensaje)
        # Retorna True confirmando que los parámetros son válidos
        return True

    def calcular_costo(
        self,
        sesiones: int = 1,
        nivel_senior: bool = False,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        """
        Método sobrescrito y sobrecargado para calcular el costo de asesoría por sesiones,
        aplicando recargo por consultor Senior y porcentajes opcionales de impuesto/descuento.
        """
        # Inicia bloque try/except/else/finally para manejo controlado de errores
        try:
            # Valida los parámetros del servicio antes de proceder al cálculo
            self.validar_parametros()
            # Verifica que el número de sesiones sea mayor a 0
            if isinstance(sesiones, bool) or not isinstance(sesiones, (int, float)) or sesiones <= 0:
                # Lanza ValueError si el número de sesiones es inválido
                raise ValueError("Las sesiones de asesoría deben ser mayores a 0.")

            # Define el factor multiplicador (1.5x para consultor Senior, 1.0x estándar)
            multiplicador = 1.5 if nivel_senior else 1.0
            # Calcula el subtotal multiplicando costo base, número de sesiones y multiplicador
            subtotal = (float(self.costo_base) * float(sesiones)) * multiplicador
            # Aplica porcentajes opcionales de descuento e impuesto
            total = self.aplicar_impuestos_y_descuentos(subtotal, impuesto, descuento)
        except (ValueError, TypeError) as e:
            # Registra el fallo en el archivo de logs
            logging.error(f"Error al calcular costo en AsesoriaEspecializada [{self.codigo}]: {e}")
            # Encadena la excepción dentro de CalculoCostoError
            raise CalculoCostoError(
                f"Cálculo inconsistente en AsesoriaEspecializada '{self.nombre_servicio}': {e}"
            ) from e
        else:
            # Registra en el archivo de logs el resultado exitoso del cálculo
            logging.info(
                f"Costo calculado en AsesoriaEspecializada [{self.codigo}]: sesiones={sesiones}, "
                f"senior={nivel_senior}, desc={descuento}%, imp={impuesto}% -> Total=${total:.2f}"
            )
            # Retorna el costo total calculado
            return total
        finally:
            # Deja registro de cierre del bloque de cálculo
            logging.debug(
                f"Finalizó ejecución de calcular_costo para AsesoriaEspecializada [{self.codigo}]."
            )

    def describir(self) -> str:
        """Método sobrescrito que retorna la descripción de la asesoría (Polimorfismo)."""
        # Devuelve una cadena formateada con los datos de la asesoría especializada
        return (
            f"Asesoría [{self.codigo}]: {self.nombre_servicio} "
            f"(Especialidad: {self.especialidad} | Tarifa: ${self.costo_base:.2f}/sesión)"
        )


# Permite probar servicio.py directamente al darle 'Run' en Visual Studio Code
if __name__ == "__main__":
    # Configura el archivo de logs para registrar la prueba directa de servicio.py
    from logger_config import configurar_logger
    configurar_logger("sistema.log")
    # Muestra en consola la prueba rápida del aporte del Integrante 2 (Servicio y ReservaSala)
    print("=== PRUEBA DIRECTA DE SERVICIO.PY (INTEGRANTE 2: Servicio y ReservaSala) ===")
    sala_prueba = ReservaSala("SALA-201", "Sala de Juntas Ejecutiva", 80.0, 25)
    print("1. Descripción:", sala_prueba.describir())
    print("2. Validación de parámetros:", sala_prueba.validar_parametros())
    print("3. Costo básico (3 horas): $", sala_prueba.calcular_costo(3))
    print("4. Costo con proyector (3 horas + $50): $", sala_prueba.calcular_costo(3, incluir_proyector=True))
    print(
        "5. Costo sobrecargado (3h + proyector, 10% desc, 19% IVA): $",
        sala_prueba.calcular_costo(3, incluir_proyector=True, impuesto=19.0, descuento=10.0),
    )
    print("=== PRUEBA DIRECTA DE SERVICIO.PY FINALIZADA SIN ERRORES ===")

