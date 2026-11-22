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

 # Devuelve el nombre del cliente
    def get_nombre(self):
        return self.__nombre

    # Devuelve el documento del cliente
    def get_documento(self):
        return self.__documento

    # Devuelve el correo del cliente
    def get_correo(self):
        return self.__correo
