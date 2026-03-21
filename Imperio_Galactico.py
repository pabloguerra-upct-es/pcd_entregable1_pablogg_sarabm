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

class StockError(Exception):
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
        if not isinstance(tripulacion, int):
            raise TypeError("tripulacion TIENE QUE SER int")
        
        if not isinstance(pasaje, int):
            raise TypeError("pasaje TIENE QUE SER int")
        
        if not isinstance(clase, EClaseNave):
            raise TypeError("clase TIENE QUE PERTENECER A EClaseNave")
        
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__clase = clase

    def transmitirMensaje(self, mensaje:str):
        super().transmitirMensaje(mensaje)
        print(f"Nave Estelar {self._idCombate}: {mensaje}")

    def obtenerClase(self):
        return self.__clase

class CazaEstelar(Nave):
    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, dotacion:int):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        self.__dotacion = dotacion

    def transmitirMensaje(self, mensaje:str):
        super().transmitirMensaje(mensaje)
        print(f"Caza Estelar {self._idCombate}: {mensaje}")

class Usuario(metaclass=ABCMeta):
    def __init__(self, idUsuario:str, nombre:str):
        if not isinstance(idUsuario, str):
            raise TypeError("idUsuario TIENE QUE SER str")
        
        if not isinstance(nombre, str):
            raise TypeError("nombre TIENE QUE SER str")
        
        self._idUsuario = idUsuario
        self._nombre = nombre

    @abstractmethod
    def iniciarSesion(self):
        pass

    @abstractmethod
    def cerrarSesion(self):
        pass

class Comandante(Usuario):
    def __init__(self, idUsuario, nombre):
        super().__init__(idUsuario, nombre)
        
        self._repuestosSolicitados = {}

    def iniciarSesion(self):
        super().iniciarSesion()
        print(f"Comandante {self._nombre} con id {self._idUsuario} ha iniciado sesion")

    def cerrarSesion(self):
        super().cerrarSesion()
        print(f"Comandante {self._nombre} con id {self._idUsuario} ha cerrado sesion")

    def consultarRepuesto(self, repuesto:Repuesto, almacen:Almacen):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE PERTENECER A LA CLASE Repuesto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen TIENE QUE PERTENECER A Almacen")
        
        if almacen.buscarRepuesto(repuesto.nombre):
            print(f"{repuesto.nombre} se encuentra en el almacen")
            return True
        
        print(f"{repuesto.nombre} no se encuentra en el almacen")
        return False

    def solicitarRepuesto(self, repuesto:Repuesto, almacen:Almacen, lista_repuestos:list, cantidad:int):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuestos TIENE QUE PERTENECER A Repuesto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen TIENE QUE PERTENECER A Almacen")
        
        if not isinstance(cantidad, int):
            raise TypeError("cantidad TIENE QUE SER int")
        
        if cantidad < 0:
            raise ValueError("cantidad DEBE SER MAYOR QUE 0")
        
        if not isinstance(cantidad, int):
            raise TypeError("cantidad TIENE QUE SER int")
        
        if self.consultarRepuesto(repuesto, almacen) == False:
            raise StockError(f"El repuesto solicitado NO se encuentra en stock")

        if almacen.cantidadRepuesto(repuesto.nombre) < cantidad:
            raise ValueError("La cantidad pedida es mayor a la habida en almacen")
        
        self._repuestosSolicitados[repuesto.nombre] = cantidad
        print(f"{repuesto.nombre} añadido a la lista de repuestos solicitados")

    def realizarPedido(self, almacen:Almacen):
        if len(self._repuestosSolicitados) == 0:
            raise EmptyError("La lista de repuestos solicitados esta vacia")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen TIENE QUE PERTENECER A Almacen")
        
        for i in self._repuestosSolicitados.keys():
            if not self.consultarRepuesto(i, almacen):
                raise StockError(f"{i.nombre} NO se encuentra ya en stock")
            
        for k, v in self._repuestosSolicitados.items():
            almacen.eliminarRepuesto(k)

        self._repuestosSolicitados = {}
            
        print("Su pedido se ha realizado con exito") 

class OperarioAlmacen(Usuario):
    def __init__(self, idUsuario, nombre):
        super().__init__(idUsuario, nombre)

    def iniciarSesion(self):
        super().iniciarSesion()
        print(f"Operario de Almacen {self._nombre} con id {self._idUsuario} ha iniciado sesion")

    def cerrarSesion(self):
        super().cerrarSesion()
        print(f"Operario de Almacen {self._nombre} con id {self._idUsuario} ha cerrado sesion")

    def añadirRepuesto(self, repuesto:Repuesto, almacen:Almacen):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE PERTENECER A Repuesto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen TIENE QUE PERTENECER A Almacen")
        
        almacen.añadirRepuesto(repuesto)

    def eliminarRepuesto(self, repuesto:Repuesto, almacen:Almacen):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE PERTENECER A Repuesto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen TIENE QUE PERTENECER A Almacen")

        almacen.eliminarRepuesto(repuesto)         

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
        self.__catalogoRepuestos = catalogoRepuestos

    def añadirRepuesto(self, repuesto:Repuesto)->None:
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE SER Repuesto")
        
        self.__catalogoRepuestos.append(repuesto)

    def eliminarRepuesto(self, repuesto:str):
        if not isinstance(repuesto, str):
            raise TypeError("repuesto TIENE QUE SER str")
        
        for i in self.__catalogoRepuestos:
            if i.nombre == repuesto:
                self.__catalogoRepuestos.remove(i)
            else:
                print(f"{repuesto} NO se encuentra en la lista de repuestos")

    def buscarRepuesto(self, repuesto:Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE SER Repuesto")
        
        for i in self.__catalogoRepuestos:
            if i.nombre == repuesto.nombre:
                return True
        return False
    
    def consultarStock(self, repuesto:Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE PERTENECER A Repuesto")
        
        if len(self.__catalogoRepuestos) == 0:
            raise StockError("El stock del almacen esta vacio")
        
        for i in self.__catalogoRepuestos:
            print(f"Nombre: {i.nombre}\tProveedor: {i.proveedor}\nPrecio: {i.precio}")

    def cantidadRepuesto(self, repuesto:Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE PERTENECER A Repuesto")
        
        if not self.buscarRepuesto(repuesto):
            raise StockError("El repuesto que buscas no se encuentra en Stock")
        
        return repuesto.__cantidad
