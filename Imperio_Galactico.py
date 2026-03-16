from enum import Enum
from abc import ABCMeta, abstractmethod

class EUbicacion(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cumulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class EClaseNave(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

class AccesoDenegado(Exception):
    pass

class UnidadCombate(metaclass=ABCMeta):
    def __init__(self, idCombate:str, claveCifrada:int):
        if not isinstance(idCombate, str):
            raise TypeError("idCombate TIENE QUE SER STR")
        
        if not isinstance(claveCifrada, int):
            raise TypeError("claveCifrada TIENE QUE SER INT")

        self._idCombate = idCombate
        self._claveCifrada = claveCifrada

    def autentificarClave(self, clave_a_verificar:int)->bool:
        if not isinstance(clave_a_verificar, int):
            raise TypeError("clave_a_verificar TIENE QUE SER INT")
        
        if clave_a_verificar == self._claveCifrada:
            print(f'CLAVE CORRECTA.\nUnidad de Combate {self._claveCifrada} autentificada correctamente')
            return True
        raise AccesoDenegado('CLAVE INCORRECTA.\nRevise la clave introducida')

    @abstractmethod
    def transmitirMensaje(self, mensaje:str)->None:
        if not isinstance(mensaje, str):
            raise TypeError("mensaje TIENE QUE SER STR")
        pass

class Nave(UnidadCombate, metaclass=ABCMeta):
    def __init__(self, idCombate, claveCifrada, nombre:str, catalogoPiezas:list[str]):
        super().__init__(idCombate, claveCifrada)
        self._nombre = nombre
        self._catalogoPiezas = catalogoPiezas

class EstacionEspacial(Nave):
    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, tripulacion:int, pasaje:int, ubicacion:EUbicacion):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        if not isinstance(tripulacion, int):
            raise TypeError("tripulacion TIENE QUE SER int")
        
        if not isinstance(pasaje, int):
            raise TypeError("pasaje TIENE QUE SER int")
        
        if not isinstance(ubicacion, EUbicacion):
            raise TypeError("ubicacion DEBE PERTENECER A EUbicacion")
        
        if tripulacion < 0 or pasaje < 0:
            raise ValueError("DEBE SER POSITIVO")
        
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__ubicacion = ubicacion

    def calcularCapacidad(self)->int:
        capacidad_total = self.__tripulacion + self.__pasaje
        return capacidad_total
    
    def actualizarUbicacion(self, nueva_ubicacion:EUbicacion)->None:
        if not isinstance(nueva_ubicacion, EUbicacion):
            raise TypeError("nueva_ubicacion DEBE PERTENECER A EUbicacion")
        self.__ubicacion = nueva_ubicacion    

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

class Usuario(metaclass=ABCMeta):
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

