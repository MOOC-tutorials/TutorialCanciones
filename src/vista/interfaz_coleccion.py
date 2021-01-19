from PyQt5.QtWidgets import QApplication
from .vista_album import Ventana_Album
from .vista_busqueda import Ventana_Inicial
from .vista_cancion import Ventana_Cancion
from .vista_interprete import Ventana_Interprete
from .vista_lista_album import Ventana_Lista_Album
from .vista_lista_cancion import Ventana_Lista_Canciones
from .vista_lista_interpretes import Ventana_Lista_Interpretes

class App(QApplication):
    def __init__(self, sys_argv, logica):
        super(App, self).__init__(sys_argv)
        
        self.logica = logica

        self.ventana_buscar = Ventana_Inicial(self)
        self.ventana_lista_album = Ventana_Lista_Album(self)
        self.ventana_album = Ventana_Album(self)
        self.ventana_lista_canciones = Ventana_Lista_Canciones(self)
        self.ventana_cancion = Ventana_Cancion(self)
        self.ventana_lista_interpretes = Ventana_Lista_Interpretes(self)
        self.ventana_interprete = Ventana_Interprete(self)
        self.mostrar_ventana_lista_albums()

    def mostrar_ventana_lista_albums(self):
        self.ventana_lista_album.show()
        self.ventana_lista_album.mostrar_albums(self.logica.darAlbumes())

    def mostrar_ventana_album(self, indice_album):
        self.ventana_album.show()
        self.ventana_album.mostrar_album(self.logica.darAlbumPorId(indice_album))
        self.ventana_album.mostrar_canciones(self.logica.darCancionesDeAlbum(indice_album))

    def mostrar_ventana_lista_canciones(self):
        self.ventana_lista_canciones.show()
        self.ventana_lista_canciones.mostrar_canciones(self.logica.darCanciones())

    def mostrar_ventana_cancion(self, id_cancion):
        self.ventana_cancion.show()
        self.ventana_cancion.mostrar_cancion(self.logica.darCancionPorId(id_cancion))

    def mostrar_ventana_buscar(self):
        self.ventana_buscar.show()

    def mostrar_ventana_lista_interpretes(self):
        self.ventana_lista_interpretes.show()
        self.ventana_lista_interpretes.mostrar_interpretes(self.logica.darInterpretes())

    def mostrar_ventana_interprete(self, n_interprete):
        self.ventana_interprete.show()
        print(n_interprete)
        self.ventana_interprete.mostrar_interprete(self.logica.darInterpretePorId(n_interprete))

    def dar_medios(self):
        return self.logica.darMedios()

    def guardar_album(self, n_album, nuevo_album):
        self.logica.editarAlbum(n_album, nuevo_album["titulo"], nuevo_album["ano"], nuevo_album["descripcion"], nuevo_album["medio"])

    def eliminar_album(self, n_album):
        self.mock_albums.pop(n_album)
        self.ventana_album.mostrar_album(0, self.mock_albums[0])

    def guardar_cancion(self, n_cancion, nueva_cancion):
        self.logica.editarCancion(n_cancion, nueva_cancion["titulo"], nueva_cancion["minutos"], nueva_cancion["segundos"], nueva_cancion["compositor"], nueva_cancion["interpretes"])

    def eliminar_cancion(self, id_cancion):
        self.ventana_cancion.hide()
        self.logica.eliminarCancion(id_cancion)
        self.ventana_lista_canciones.mostrar_canciones(self.logica.darCanciones())

    def crear_album(self, nuevo_album):
        self.logica.agregarAlbum(nuevo_album["titulo"], nuevo_album["ano"], nuevo_album["descripcion"], nuevo_album["medio"])
        self.ventana_lista_album.mostrar_albums(self.logica.darAlbumes())

    def guardar_interprete(self, n_interprete, nuevo_interprete):
        self.logica.editarInterprete(n_interprete, nuevo_interprete)
        self.ventana_interprete.hide()
        self.mostrar_ventana_lista_interpretes()
    
    def eliminar_interprete(self, n_interprete):
        self.logica.eliminarInterprete(n_interprete)
        self.ventana_interprete.hide()
        self.mostrar_ventana_lista_interpretes()

    def crear_interprete(self, nuevo_interprete):
        self.logica.agregarInterprete(nuevo_interprete)
        self.mostrar_ventana_lista_interpretes()

    def crear_cancion(self, nueva_cancion):
        self.logica.agregarCancion(nueva_cancion["Titulo"],nueva_cancion["Minutos"], nueva_cancion["Segundos"], nueva_cancion["Compositor"])
        self.mostrar_ventana_lista_canciones()

    def mostrar_resultados_albumes(self, nombre_album):
        albumes = self.logica.buscarAlbumesPorTitulo(nombre_album)
        self.ventana_buscar.mostrar_resultados_albumes(albumes)

    def mostrar_resultados_canciones(self, nombre_cancion):
        canciones = self.logica.buscarCancionesPorTitulo(nombre_cancion)
        self.ventana_buscar.mostrar_resultados_canciones(canciones)

    def mostrar_resultados_interpretes(self, nombre_interprete):
        interpretes = self.logica.buscarInterpretesPorNombre(nombre_interprete)
        self.ventana_buscar.mostrar_resultados_interpretes(interpretes)

    def quitar_cancion_de_album(self, id_cancion, id_album):
        pass

    
