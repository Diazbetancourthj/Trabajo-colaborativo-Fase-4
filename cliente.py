class Cliente:
    def __init__(self, nombre, documento, correo):
        # Atributos privados (encapsulación)
        self.__nombre = ""
        self.__documento = ""
        self.__correo = ""

        # Se usan los set para que se validen los datos
        self.set_nombre(nombre)
        self.set_documento(documento)
        self.set_correo(correo)
