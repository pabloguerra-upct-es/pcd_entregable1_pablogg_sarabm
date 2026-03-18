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

class EmptyError(Exception):
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

class Repuesto:
    def __init__(self, nombre:str, proveedor:str, cantidad:int, precio:float):
        if not isinstance(nombre, str):
            raise TypeError("nombre TIENE QUE SER str")
        
        if not isinstance(proveedor, str):
            raise TypeError("proveedor TIENE QUE SER str")
        
        if not isinstance(cantidad, int):
            raise TypeError("cantidad TIENE QUE SER int")
        
        if not isinstance(precio, (int, float)):
            raise TypeError("precio TIENE QUE SER float")
        
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio
    
    def obtenerUnidades(self):
        return self.__cantidad
    
    def aumentarStock(self, cantidad_aumentar:int):
        if not isinstance(cantidad_aumentar, int):
            raise TypeError("cantidad_aumentar TIENE QUE SER int")
        
        self.__cantidad += cantidad_aumentar

    def reducirStock(self, cantidad_disminuir:int):
        if not isinstance(cantidad_disminuir, int):
            raise TypeError("cantidad_disminuir TIENE QUE SER int")
        
        if cantidad_disminuir > self.__cantidad:
            raise ValueError("La cantidad a disminuir es mayor que la cantidad actual en stock")
    
        self.__cantidad -= cantidad_disminuir

class Nave(UnidadCombate, metaclass=ABCMeta):
    def __init__(self, idCombate, claveCifrada, nombre:str, catalogoPiezas:list[str]):
        super().__init__(idCombate, claveCifrada)
        self._nombre = nombre
        self._catalogoPiezas = catalogoPiezas

    @abstractmethod
    def transmitirMensaje(self, mensaje: str):
        pass

    def consultarCatalogo(self):
        if len(self._catalogoPiezas) == 0:
            raise EmptyError("El catalogo esta vacio")
        
        return self._catalogoPiezas
    
    def solicitarRepuesto(self, repuesto:Repuesto, cantidad:int):

        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE SER Repuesto")
        
        if not isinstance(cantidad, int):
            raise TypeError("cantidad TIENE QUE SER int")
        
        if repuesto.nombre not in self._catalogoPiezas:
            print(f"{repuesto.nombre} NO se encuentra en el catalogo de repuestos disponibles")
            return False

        cantidad_stock = repuesto.obtenerUnidades()

        if cantidad > cantidad_stock:
            print(f"No hay suficientes {repuesto.nombre} en stock")
            return False
        
        repuesto.reducirStock(cantidad)
        return True

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

    def transmitirMensaje(self, mensaje:str):
        super().transmitirMensaje(mensaje)
        print(f"Estacion Estelar {self._idCombate}: {mensaje}")

class NaveEstelar(Nave):
    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, tripulacion:int, pasaje:int, clase:EClaseNave):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__clase = clase

    def transmitirMensaje(self, mensaje:str):
        super().transmitirMensaje(mensaje)
        print(f"Nave Estelar {self._idCombate}: {mensaje}")

class CazaEstelar(Nave):
    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, dotacion:int):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        self.__dotacion = dotacion

    def transmitirMensaje(self, mensaje:str):
        super().transmitirMensaje(mensaje)
        print(f"Caza Estelar {self._idCombate}: {mensaje}")

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

class Almacen:
    def __init__(self, nombre:str, ubicacion:str, catalogoRepuestos:list[Repuesto]):
        if not isinstance(nombre, str):
            raise TypeError("nombre TIENE QUE SER str")
        
        if not isinstance(ubicacion, str):
            raise TypeError("ubicacion TIENE QUE SER str")
        
        if not all(isinstance(r, Repuesto) for r in catalogoRepuestos):
                    raise TypeError("El catálogo solo debe contener objetos Repuesto")
        
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.__catalogoRepuestos = list(Repuesto)

    def añadirRepuesto(self, repuesto:Repuesto)->None:
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE SER Repuesto")
        
        self.__catalogoRepuestos.append(repuesto)

    def eliminarRepuesto(self, repuesto:Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE SER Repuesto")
        
        for i in self.__catalogoRepuestos:
            if i.nombre == repuesto.nombre:
                self.__catalogoRepuestos.pop(i)
            else:
                print(f"{repuesto.nombre} NO se encuentra en la lista de repuestos")

    def buscarRepuesto(self, repuesto:Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE SER Repuesto")
        
        for i in self.__catalogoRepuestos:
            if i.nombre == repuesto.nombre:
                return True
        return False

    

