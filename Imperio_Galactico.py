from enum import Enum

class EUbicacion(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cumulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class EClaseNave(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

class UnidadCombate:
    def __init__(self, idCombate:str, claveCifrada:int):
        self._idCombate = idCombate
        self._claveCifrada = claveCifrada

class Nave(UnidadCombate):
    def __init__(self, idCombate, claveCifrada, nombre:str, catalogoPiezas:list[str]):
        super().__init__(idCombate, claveCifrada)
        self._nombre = nombre
        self._catalogoPiezas = catalogoPiezas

class EstacionEspacial(Nave):
    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, tripulacion:int, pasaje:int, ubicacion:EUbicacion):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__ubicacion = ubicacion

class NaveEstelar(Nave):
    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, tripulacion:int, pasaje:int, clase:EClaseNave):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__clase = clase

class CazaEstelar(Nave):
    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, dotacion:int):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        self.__dotacion = dotacion

class Usuario:
    def __init__(self, idUsuario:str, nombre:str):
        self._idUsuario = idUsuario
        self._nombre = nombre

class Comandante(Usuario):
    def __init__(self, idUsuario, nombre):
        super().__init__(idUsuario, nombre)

class OperarioAlmacen(Usuario):
    def __init__(self, idUsuario, nombre):
        super().__init__(idUsuario, nombre)

class Repuesto:
    def __init__(self, nombre:str, proveedor:str, cantidad:int, precio:float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio

class Almacen:
    def __init__(self, nombre:str, ubicacion:str, catalogoRepuestos:list[Repuesto]):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.__catalogoRepuestos = catalogoRepuestos

