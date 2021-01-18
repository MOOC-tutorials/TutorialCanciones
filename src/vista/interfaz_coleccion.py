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

        self.mock_albums = [{"Titulo":"Caribe Atómico", "Intérpretes":"Aterciopelados", "Medio":"CD", "Anio":1998, "Descripcion":"Las canciones que me gustan"},
                          {"Titulo":"Corazones", "Intérpretes":"Los Prisioneros", "Medio":"Acetato", "Anio":1999, "Descripcion":"Las canciones que NO me gustan"},
                          {"Titulo":"Pateando Piedras", "Intérpretes":"Los Prisioneros", "Medio":"CD", "Anio":2001, "Descripcion":"Las canciones que meh"},
                          {"Titulo":"Pateando Piedras", "Intérpretes":"Los Prisioneros", "Medio":"Casette", "Anio":1995, "Descripcion":"Las canciones que casi me gustan"}]

        self.mock_canciones = [{"Titulo":"El estuche", "Intérpretes":"Aterciopelados", "Duracion":"3:10", "Compositor":"Andrea Echeverri"},
                          {"Titulo":"Maligno", "Intérpretes":"Aterciopelados", "Duracion":"3:25", "Compositor":"Andrea Echeverri"},
                          {"Titulo":"Caribe atómico", "Intérpretes":"Aterciopelados", "Duracion":"4:02", "Compositor":"Andrea Echeverri"},
                         ]
                         
        self.mock_interpretes = ["Aterciopelados", "Los Prisioneros"]

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

    def mostrar_ventana_album(self, n_album):
        self.ventana_album.show()
        self.ventana_album.mostrar_album(n_album, self.logica.darAlbumes()[n_album-1])
        self.ventana_album.mostrar_canciones(self.mock_canciones)

    def mostrar_ventana_lista_canciones(self):
        self.ventana_lista_canciones.show()
        self.ventana_lista_canciones.mostrar_canciones(self.coleccion.darCanciones())

    def mostrar_ventana_cancion(self, n_cancion):
        self.ventana_cancion.show()
        self.ventana_cancion.mostrar_cancion(n_cancion, self.mock_canciones[n_cancion])

    def mostrar_ventana_buscar(self):
        self.ventana_buscar.show()

    def mostrar_ventana_lista_interpretes(self):
        self.ventana_lista_interpretes.show()
        self.ventana_lista_interpretes.mostrar_interpretes(self.logica.darInterpretes())

    def mostrar_ventana_interprete(self, interprete):
        self.ventana_interprete.show()
        self.ventana_interprete.mostrar_interprete(interprete)

    def dar_medios(self):
        return ["CD", "Acetato", "Casette"]

    def guardar_album(self, n_album, album_a_insertar):
        self.mock_albums[n_album:n_album+1] = [album_a_insertar]

    def eliminar_album(self, n_album):
        self.mock_albums.pop(n_album)
        self.ventana_album.mostrar_album(0, self.mock_albums[0])

    def guardar_cancion(self, n_cancion, cancion_a_insertar):
        self.mock_canciones[n_cancion:n_cancion+1] = [cancion_a_insertar]
        self.ventana_cancion.hide()
        self.mostrar_ventana_lista_canciones()

    def eliminar_cancion(self, n_cancion):
        del self.mock_canciones[n_cancion]
        self.ventana_cancion.hide()
        self.mostrar_ventana_lista_canciones()

    def crear_album(self, nuevo_album):
        self.logica.agregarAlbum(nuevo_album["titulo"], nuevo_album["ano"], nuevo_album["descripcion"], nuevo_album["medio"])
        self.ventana_lista_album.mostrar_albums(self.mock_albums)

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
        self.coleccion.agregarCancion(nueva_cancion["Titulo"],nueva_cancion["Minutos"], nueva_cancion["Segundos"], nueva_cancion["Compositor"], -1, -1)
        


    
