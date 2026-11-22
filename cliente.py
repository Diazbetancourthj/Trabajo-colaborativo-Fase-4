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

# Revisa que el nombre sea correcto
    def validar_nombre(self, nombre):
        # El nombre no puede ser None ni estar vacío
        if nombre is None or nombre.strip() == "":
            raise DatoInvalidoError("El nombre no puede estar vacío")

        # El nombre debe tener mínimo 3 letras
        if len(nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 letras")

        # Se quitan los espacios para revisar que todo lo demás sean letras
        if not nombre.replace(" ", "").isalpha():
            raise DatoInvalidoError("El nombre solo puede tener letras y espacios")

        # Si pasó todas las revisiones, el nombre es válido
        return True

    # Revisa que el documento sea correcto
    def validar_documento(self, documento):
        # El documento no puede ser None ni estar vacío
        if documento is None or str(documento).strip() == "":
            raise DatoInvalidoError("El documento no puede estar vacío")

        # Se intenta convertir a número para saber si son solo dígitos
        try:
            int(documento)
        except ValueError as error:
            # Se lanza nuestra excepción guardando el error original
            # (esto es el encadenamiento de excepciones)
            raise DatoInvalidoError("El documento debe contener solo números") from error

        # El documento debe tener entre 6 y 10 dígitos
        if len(str(documento)) < 6 or len(str(documento)) > 10:
            raise DatoInvalidoError("El documento debe tener entre 6 y 10 dígitos")

        # Si pasó todas las revisiones, el documento es válido
        return True

    # Revisa que el correo sea correcto
    def validar_correo(self, correo):
        # El correo no puede ser None ni estar vacío
        if correo is None or correo.strip() == "":
            raise DatoInvalidoError("El correo no puede estar vacío")

        # El correo no puede tener espacios
        if " " in correo:
            raise DatoInvalidoError("El correo no puede tener espacios")

        # El correo debe tener exactamente un @
        if correo.count("@") != 1:
            raise DatoInvalidoError("El correo debe tener un solo @")

        # Se separa el correo en dos partes: antes y después del @
        partes = correo.split("@")

        # Antes del @ debe haber algo y después del @ debe haber un punto
        if partes[0] == "" or "." not in partes[1]:
            raise DatoInvalidoError("El correo no tiene un formato válido")

        # Si pasó todas las revisiones, el correo es válido
        return True

    # Muestra en pantalla los datos del cliente
    def mostrar_datos(self):
        print("Cliente:", self.__nombre)
        print("Documento:", self.__documento)
        print("Correo:", self.__correo)

