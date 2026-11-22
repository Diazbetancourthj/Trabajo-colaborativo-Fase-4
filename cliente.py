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

  # Cambia el nombre solo si es válido
    def set_nombre(self, nombre):
        # Si el nombre no es válido, validar_nombre lanza una excepción
        # y la línea de abajo no se ejecuta
        self.validar_nombre(nombre)
        self.__nombre = nombre

    # Cambia el documento solo si es válido
    def set_documento(self, documento):
        self.validar_documento(documento)
        self.__documento = documento

    # Cambia el correo solo si es válido
    def set_correo(self, correo):
        self.validar_correo(correo)
        self.__correo = correo
