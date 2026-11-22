# Módulo: simulacion.py
# Descripción: Gestiona las listas internas en memoria (clientes, servicios y
#              reservas) sin uso de bases de datos, y ejecuta la simulación
#              secuencial de más de 10 operaciones completas (válidas y fallidas)
#              para demostrar la estabilidad y robustez del sistema Software FJ.
# ==============================================================================

# Importa os y sys para asegurar la resolución de módulos locales en cualquier entorno o IDE
import os
import sys

# Inserta el directorio del archivo actual en sys.path
if "__file__" in globals():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa el módulo logging para registrar el avance de la simulación en sistema.log
import logging
# Importa la clase Cliente para la creación y validación de clientes
from cliente import Cliente
# Importa la clase abstracta Servicio y las 3 subclases especializadas
from servicio import (
    Servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
# Importa la clase Reserva para gestionar confirmaciones y cancelaciones
from reserva import Reserva
# Importa las excepciones personalizadas para capturarlas de forma controlada
from excepciones import (
    SoftwareFJError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaError,
)


class SistemaSoftwareFJ:
    """Clase gestora que administra las listas internas de clientes, servicios y reservas."""

    def __init__(self):
        """Inicializa las listas internas en memoria para gestionar objetos sin base de datos."""
        # Lista interna que almacena los objetos Cliente registrados exitosamente
        self.lista_clientes = []
        # Lista interna que almacena los objetos Servicio (salas, equipos, asesorías) válidos
        self.lista_servicios = []
        # Lista interna que almacena todas las instancias de Reserva procesadas
        self.lista_reservas = []
        # Registra en el archivo de logs la inicialización del gestor en memoria
        logging.info("Gestor SistemaSoftwareFJ inicializado con listas internas en memoria.")

    def registrar_cliente(self, nombre: str, documento: str, correo: str):
        """Intenta crear y agregar un cliente a la lista interna usando try/except/else."""
        # Inicia bloque try/except/else para evitar que un dato inválido detenga el sistema
        try:
            # Instancia el objeto Cliente (ejecuta internamente las validaciones estrictas)
            nuevo_cliente = Cliente(nombre, documento, correo)
        except ClienteInvalidoError as e:
            print(f" [ERROR CLIENTE] Registro rechazado -> {e}")
            logging.error(f"Registro de cliente rechazado: {e}")
            return None
        else:
            # Agrega el cliente válido a la lista interna en memoria
            self.lista_clientes.append(nuevo_cliente)
            # Muestra en consola la confirmación de registro exitoso del cliente
            print(f" [CLIENTE OK] {nuevo_cliente.mostrar_datos()}")
            # Retorna la instancia del cliente creado
            return nuevo_cliente

    def registrar_servicio(self, clase_servicio, *args, **kwargs):
        """Intenta instanciar y agregar un servicio especializado a la lista interna."""
        # Inicia bloque try/except/else para capturar errores en parámetros del servicio
        try:
            # Instancia polimórficamente la subclase de Servicio solicitada
            nuevo_servicio = clase_servicio(*args, **kwargs)
        except ServicioInvalidoError as e:
            print(f" [ERROR SERVICIO] Creación rechazada -> {e}")
            logging.error(f"Creación de servicio rechazada: {e}")
            return None
        else:
            # Almacena el servicio válido en la lista interna de servicios
            self.lista_servicios.append(nuevo_servicio)
            # Imprime en consola la descripción polimórfica del servicio creado
            print(f" [SERVICIO OK] {nuevo_servicio.describir()}")
            # Retorna la instancia del servicio creado
            return nuevo_servicio

    def crear_y_confirmar_reserva(
        self, cliente: Cliente, servicio: Servicio, *args, **kwargs
    ) -> Reserva:
        """Crea una reserva, la almacena en la lista interna e intenta confirmarla."""
        # Crea la instancia de Reserva vinculando el cliente y el servicio
        nueva_reserva = Reserva(cliente, servicio)
        # Almacena la reserva en la lista interna para mantener trazabilidad completa
        self.lista_reservas.append(nueva_reserva)
        # Inicia bloque try/except para capturar cualquier ReservaError encadenado
        try:
            # Invoca confirmar() pasando los parámetros posicionales y opcionales (sobrecarga)
            nueva_reserva.confirmar(*args, **kwargs)
        except ReservaError as e:
            # Muestra el error encadenado y la causa raíz (__cause__) sin detener el programa
            causa = f" | Causa raíz: {type(e.__cause__).__name__}: {e.__cause__}" if e.__cause__ else ""
            # Imprime el detalle del fallo controlado en consola
            print(f" [ERROR RESERVA] {e}{causa}")
        # Retorna la instancia de la reserva (ya sea Confirmada o Fallida)
        return nueva_reserva

    def mostrar_resumen_listas(self) -> None:
        """Imprime el estado final de todas las listas internas del sistema."""
        # Imprime separador visual del resumen general en consola
        print("\n" + "=" * 85)
        # Imprime el título de la sección de resumen de listas en memoria
        print(" RESUMEN DE OBJETOS ALMACENADOS EN LISTAS INTERNAS (SIN BASE DE DATOS)")
        # Imprime separador visual
        print("=" * 85)

        # Muestra el total de clientes válidos almacenados en la lista interna
        print(f"\n1. Clientes Válidos Registrados ({len(self.lista_clientes)}):")
        # Recorre cada objeto Cliente en la lista interna
        for idx, cli in enumerate(self.lista_clientes, start=1):
            # Imprime los datos encapsulados del cliente mediante mostrar_datos()
            print(f"   {idx}. {cli.mostrar_datos()}")

        # Muestra el total de servicios válidos almacenados en la lista interna
        print(f"\n2. Servicios Especializados Activos ({len(self.lista_servicios)}):")
        # Recorre cada objeto Servicio en la lista interna aplicando polimorfismo
        for idx, srv in enumerate(self.lista_servicios, start=1):
            # Imprime la descripción polimórfica de cada servicio
            print(f"   {idx}. {srv.describir()}")

        # Muestra el total de reservas registradas en la lista interna
        print(f"\n3. Historial de Reservas Procesadas ({len(self.lista_reservas)}):")
        # Recorre cada objeto Reserva almacenado en la lista interna
        for idx, res in enumerate(self.lista_reservas, start=1):
            # Imprime el detalle completo de la reserva y su estado final
            print(f"   {idx}. {res.mostrar_reserva()}")
        # Imprime línea de cierre del resumen
        print("=" * 85 + "\n")


def validar_segmento_integrante_2() -> None:
    """
    Ejecuta secuencialmente el segmento de código del Integrante 2 (Clases Servicio
    y ReservaSala) para validar su funcionamiento, polimorfismo y sobrecarga.
    """
    # Registra el inicio de la validación secuencial del Integrante 2 en el log
    logging.info("Iniciando validación secuencial del segmento del Integrante 2 (Servicio y ReservaSala).")
    # Imprime encabezado de validación del aporte del Integrante 2
    print("\n" + "#" * 85)
    # Muestra el título del segmento correspondiente al Integrante 2
    print(" VALIDACIÓN SECUENCIAL DEL SEGMENTO DEL INTEGRANTE 2: Servicio y ReservaSala")
    # Imprime línea divisoria
    print("#" * 85)

    # 1. Prueba de creación e invocación de métodos de ReservaSala (Integrante 2)
    print("\n[Prueba 2.1] Creación de ReservaSala válida y uso de describir() y validar_parametros():")
    # Instancia un objeto ReservaSala con código, nombre, costo base ($80/h) y capacidad (25 personas)
    sala_juntas = ReservaSala("SALA-201", "Sala de Juntas Ejecutiva", 80.0, 25)
    # Imprime la descripción polimórfica de la sala creada
    print(f" -> Descripción: {sala_juntas.describir()}")
    # Imprime el resultado de la validación explícita de parámetros
    print(f" -> ¿Parámetros válidos?: {sala_juntas.validar_parametros()}")

    # 2. Prueba de sobrecarga en calcular_costo() de ReservaSala (Integrante 2)
    print("\n[Prueba 2.2] Variantes sobrecargadas de calcular_costo() en ReservaSala:")
    # Variante A: Solo horas (3 horas * $80 = $240.0)
    costo_basico = sala_juntas.calcular_costo(horas=3)
    # Imprime el resultado de la variante básica
    print(f" -> Variante A (3 horas sin adicionales): ${costo_basico:.2f}")
    # Variante B: Horas + proyector opcional (3 horas * $80 + $50 proyector = $290.0)
    costo_proyector = sala_juntas.calcular_costo(horas=3, incluir_proyector=True)
    # Imprime el resultado de la variante con proyector
    print(f" -> Variante B (3 horas + proyector $50): ${costo_proyector:.2f}")
    # Variante C: Horas + proyector + descuento (10%) + impuesto IVA (19%)
    costo_completo = sala_juntas.calcular_costo(
        horas=3, incluir_proyector=True, impuesto=19.0, descuento=10.0
    )
    # Imprime el resultado de la variante sobrecargada con descuento e impuestos
    print(f" -> Variante C (3 horas + proyector, 10% desc., 19% IVA): ${costo_completo:.2f}")

    # 3. Prueba de validación de error en ReservaSala por capacidad inválida (Integrante 2)
    print("\n[Prueba 2.3] Control de excepción en ReservaSala por capacidad inválida (<= 0):")
    # Inicia bloque try/except para capturar ServicioInvalidoError sin detener la ejecución
    try:
        # Intenta crear una sala con capacidad negativa (-5 personas)
        ReservaSala("SALA-ERR", "Sala Defectuosa", 60.0, -5)
    except ServicioInvalidoError as e:
        # Muestra que la excepción de ReservaSala fue capturada correctamente
        print(f" -> Excepción capturada exitosamente: {e}")


def ejecutar_simulacion() -> SistemaSoftwareFJ:
    """
    Simula 13 operaciones completas (registros válidos e inválidos de clientes,
    creación correcta e incorrecta de servicios, y reservas exitosas y fallidas).
    """
    # Ejecuta primero la validación secuencial del segmento del Integrante 2
    validar_segmento_integrante_2()

    # Instancia el sistema gestor basado en listas internas
    sistema = SistemaSoftwareFJ()

    # Imprime el encabezado principal de las 12 operaciones de simulación
    print("\n" + "#" * 85)
    # Muestra el título de la simulación integral requerida por el Anexo 3
    print(" SIMULACIÓN INTEGRAL DE 12 OPERACIONES COMPLETAS - EMPRESA SOFTWARE FJ")
    # Imprime línea divisoria
    print("#" * 85)

    # --------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de clientes (Almacenados en lista interna)
    # --------------------------------------------------------------------------
    print("\n--- [OPERACIÓN 1] Registro válido de clientes en el sistema ---")
    # Registra al primer cliente válido (Carlos Mendoza)
    cli_carlos = sistema.registrar_cliente("Carlos Mendoza", "1020304050", "carlos.mendoza@unad.edu.co")
    # Registra a la segunda cliente válida (Laura Gómez)
    cli_laura = sistema.registrar_cliente("Laura Gómez", "1098765432", "laura.gomez@empresa.com")

    # --------------------------------------------------------------------------
    # OPERACIÓN 2: Intento de registro inválido de cliente (Documento no numérico)
    # --------------------------------------------------------------------------
    print("\n--- [OPERACIÓN 2] Intento de registro de cliente con documento inválido ---")
    # Intenta registrar un cliente con letras en el número de documento (debe fallar controladamente)
    sistema.registrar_cliente("Pedro Pérez", "ABC-999", "pedro.perez@correo.com")

    # --------------------------------------------------------------------------
    # OPERACIÓN 3: Intento de registro inválido de cliente (Correo mal formado)
    # --------------------------------------------------------------------------
    print("\n--- [OPERACIÓN 3] Intento de registro de cliente con correo electrónico inválido ---")
    # Intenta registrar un cliente con un correo sin dominio ni símbolo @ válido
    sistema.registrar_cliente("Ana Martínez", "1055667788", "ana.martinez_correo_invalido")

    # --------------------------------------------------------------------------
    # OPERACIÓN 4: Creación correcta de los 3 servicios especializados (Polimorfismo)
    # --------------------------------------------------------------------------
    print("\n--- [OPERACIÓN 4] Creación válida de los 3 tipos de servicios especializados ---")
    # Crea un servicio ReservaSala válido (Integrante 2)
    srv_sala = sistema.registrar_servicio(
        ReservaSala, "SALA-101", "Auditorio Principal Innovación", 120.0, 50
    )
    # Crea un servicio AlquilerEquipo válido (Integrante 3)
    srv_equipo = sistema.registrar_servicio(
        AlquilerEquipo, "EQP-202", "Servidor GPU DeepLearning", 150.0, "Workstation RTX"
    )
    # Crea un servicio AsesoriaEspecializada válido (Integrante 4)
    srv_asesoria = sistema.registrar_servicio(
        AsesoriaEspecializada, "ASE-303", "Consultoría Arquitectura Cloud", 200.0, " Ciberseguridad y Nube"
    )

    # --------------------------------------------------------------------------
    # OPERACIÓN 5: Creación incorrecta de servicio (Costo base negativo)
    # --------------------------------------------------------------------------
    print("\n--- [OPERACIÓN 5] Intento de creación de servicio con costo base negativo ---")
    # Intenta crear una sala con costo base de -$90.0 (lanza ServicioInvalidoError)
    sistema.registrar_servicio(ReservaSala, "SALA-999", "Sala Costo Negativo", -90.0, 15)

    # --------------------------------------------------------------------------
    # OPERACIÓN 6: Creación incorrecta de servicio (Capacidad inválida en ReservaSala)
    # --------------------------------------------------------------------------
    print("\n--- [OPERACIÓN 6] Intento de creación de ReservaSala con capacidad cero ---")
    # Intenta crear una sala con capacidad 0 (validación polimórfica de ReservaSala - Integrante 2)
    sistema.registrar_servicio(ReservaSala, "SALA-000", "Sala Sin Capacidad", 75.0, 0)

    # --------------------------------------------------------------------------
    # OPERACIÓN 7: Reserva exitosa de Sala con sobrecarga (Proyector + IVA + Descuento)
    # --------------------------------------------------------------------------
    print("\n--- [OPERACIÓN 7] Reserva exitosa de ReservaSala con proyector, descuento e IVA ---")
    # Procesa reserva de 4 horas con proyector ($50), descuento del 5% e IVA del 19%
    res_sala_ok = sistema.crear_y_confirmar_reserva(
        cli_carlos, srv_sala, 4, incluir_proyector=True, impuesto=19.0, descuento=5.0
    )

    # --------------------------------------------------------------------------
    # OPERACIÓN 8: Reserva exitosa de Alquiler de Equipo con seguro contra daños
    # --------------------------------------------------------------------------
    print("--- [OPERACIÓN 8] Reserva exitosa de AlquilerEquipo por 3 días con seguro ---")
    # Procesa reserva de equipo por 3 días incluyendo póliza de seguro contra daños
    res_equipo_ok = sistema.crear_y_confirmar_reserva(
        cli_laura, srv_equipo, 3, seguro_danos=True, impuesto=19.0
    )

    # --------------------------------------------------------------------------
    # OPERACIÓN 9: Reserva exitosa de Asesoría Especializada Nivel Senior
    # --------------------------------------------------------------------------
    print("--- [OPERACIÓN 9] Reserva exitosa de AsesoriaEspecializada (2 sesiones Senior) ---")
    # Procesa reserva de 2 sesiones de asesoría con especialista nivel Senior (multiplicador 1.5x)
    res_asesoria_ok = sistema.crear_y_confirmar_reserva(
        cli_carlos, srv_asesoria, 2, nivel_senior=True, descuento=10.0
    )

    # --------------------------------------------------------------------------
    # OPERACIÓN 10: Reserva fallida por duración inválida (Horas <= 0 en ReservaSala)
    # --------------------------------------------------------------------------
    print("--- [OPERACIÓN 10] Intento de reserva fallida con horas negativas (-2 horas) ---")
    # Intenta confirmar una reserva de sala con -2 horas (demuestra encadenamiento de excepciones)
    res_fallida_horas = sistema.crear_y_confirmar_reserva(
        cli_laura, srv_sala, -2, incluir_proyector=False
    )

    # --------------------------------------------------------------------------
    # OPERACIÓN 11: Reserva fallida por porcentaje de descuento inconsistente (> 100%)
    # --------------------------------------------------------------------------
    print("--- [OPERACIÓN 11] Intento de reserva fallida por descuento inconsistente (150%) ---")
    # Intenta confirmar una reserva aplicando 150% de descuento (lanza CalculoCostoError encadenado)
    sistema.crear_y_confirmar_reserva(
        cli_carlos, srv_equipo, 2, seguro_danos=False, descuento=150.0
    )

    # --------------------------------------------------------------------------
    # OPERACIÓN 12: Cancelación exitosa de reserva confirmada vs. cancelación rechazada
    # --------------------------------------------------------------------------
    print("--- [OPERACIÓN 12] Cancelación de reserva confirmada y rechazo en reserva fallida ---")
    # Cancela exitosamente la reserva de equipo que estaba en estado 'Confirmada'
    res_equipo_ok.cancelar()
    # Intenta cancelar una reserva que quedó en estado 'Fallida' (captura OperacionNoPermitidaError)
    try:
        # Invoca cancelar() sobre res_fallida_horas cuyo estado es 'Fallida'
        res_fallida_horas.cancelar()
    except ReservaError as e:
        # Muestra cómo el sistema captura la excepción encadenada y sigue activo
        print(f" [CONTROLADO] Excepción capturada al intentar cancelar reserva no confirmada: {e}")

    # OPERACIÓN 13: Reserva fallida porque el servicio no está disponible
    print("--- [OPERACIÓN 13] Intento de reserva de un servicio no disponible ---")
    srv_asesoria.disponible = False
    sistema.crear_y_confirmar_reserva(cli_laura, srv_asesoria, 1)
    srv_asesoria.disponible = True
    
    # Muestra el resumen consolidado de objetos en las listas internas
    sistema.mostrar_resumen_listas()
    # Registra en el archivo de logs la finalización exitosa de las 12 operaciones
    logging.info("Simulación de 12 operaciones completada sin interrupciones.")
    # Retorna la instancia del sistema con todas las listas pobladas
    return sistema


# Permite ejecutar simulacion.py directamente desde Visual Studio Code o la terminal
if __name__ == "__main__":
    # Importa y configura el logger antes de iniciar la simulación directa
    from logger_config import configurar_logger
    configurar_logger("sistema.log")
    # Ejecuta la simulación completa de las 12 operaciones
    ejecutar_simulacion()
