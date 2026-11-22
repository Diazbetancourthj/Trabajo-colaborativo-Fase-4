from abc import ABC, abstractmethod
from excepciones import ServicioInvalidoError, CalculoCostoError


class Servicio(ABC):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float):
        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
        self.disponible = True

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

 # Aplica descuento e impuesto al subtotal (los usan las 3 subclases)
    def aplicar_descuento_impuesto(self, subtotal: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if descuento < 0 or descuento > 100:
            raise CalculoCostoError("El descuento debe estar entre 0 y 100.")
        if impuesto < 0:
            raise CalculoCostoError("El impuesto no puede ser negativo.")
        subtotal = subtotal - subtotal * descuento / 100
        return subtotal + subtotal * impuesto / 100

# ReservaSala 
class ReservaSala(Servicio):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, capacidad: int):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.capacidad = capacidad
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        super().validar_parametros()
        if self.capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser mayor a 0.")
        return True

    def calcular_costo(self, horas: int, incluir_proyector: bool = False,
                       impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if horas <= 0:
            raise CalculoCostoError("Las horas deben ser mayores a 0.")
        total = self.costo_base * horas
        if incluir_proyector:
            total += 50.0
        return self.aplicar_descuento_impuesto(total, impuesto, descuento)

    def describir(self) -> str:
        return f"Sala: {self.nombre_servicio} (Capacidad: {self.capacidad})"



# AlquilerEquipo 
class AlquilerEquipo(Servicio):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, tipo_hardware: str):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.tipo_hardware = tipo_hardware
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        super().validar_parametros()
        if self.tipo_hardware.strip() == "":
            raise ServicioInvalidoError("El tipo de hardware no puede estar vacío.")
        return True

    def calcular_costo(self, dias: int, seguro_danos: bool = False,
                       impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if dias <= 0:
            raise CalculoCostoError("Los días deben ser mayores a 0.")
        total = self.costo_base * dias
        if seguro_danos:
            total += 30.0 * dias
        return self.aplicar_descuento_impuesto(total, impuesto, descuento)

    def describir(self) -> str:
        return f"Equipo: {self.nombre_servicio} ({self.tipo_hardware})"


# AsesoriaEspecializada 
class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, especialidad: str):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.especialidad = especialidad
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        super().validar_parametros()
        if self.especialidad.strip() == "":
            raise ServicioInvalidoError("La especialidad no puede estar vacía.")
        return True

    def calcular_costo(self, sesiones: int, nivel_senior: bool = False,
                       impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if sesiones <= 0:
            raise CalculoCostoError("Las sesiones deben ser mayores a 0.")
        mult = 1.5 if nivel_senior else 1.0
        total = (self.costo_base * sesiones) * mult
        return self.aplicar_descuento_impuesto(total, impuesto, descuento)

    def describir(self) -> str:
        return f"Asesoría: {self.nombre_servicio} ({self.especialidad})"
