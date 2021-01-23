from PyQt5.QtWidgets import QApplication
from src.vista.vista_album import Ventana_Album
from src.vista.vista_busqueda import Ventana_Inicial
from src.vista.vista_cancion import Ventana_Cancion
from src.vista.vista_lista_album import Ventana_Lista_Album
from src.vista.vista_lista_cancion import Ventana_Lista_Canciones


class App(QApplication):
    '''
    Clase principal de la interfaz
    '''

    def __init__(self, sys_argv, logica):
        '''
        Constructor de la interfaz
        '''
        super(App, self).__init__(sys_argv)
        
        #Lógica de la aplicación
        self.logica = logica

        #Se inicializan todas las ventanas
        self.ventana_buscar = Ventana_Inicial(self)
        self.ventana_lista_album = Ventana_Lista_Album(self)
        self.ventana_album = Ventana_Album(self)
        self.ventana_lista_canciones = Ventana_Lista_Canciones(self)
        self.ventana_cancion = Ventana_Cancion(self)

        #Se comienza en la lista de albums
        self.mostrar_ventana_lista_albums()

    def mostrar_ventana_lista_albums(self):
        '''
        Método para mostrar la ventana de la lista de albums
        '''
        self.ventana_lista_album.show()
        self.ventana_lista_album.mostrar_albums(self.logica.darAlbumes())

    def mostrar_ventana_album(self, indice_album):
        '''
        Método para mostrar un album en particular
        '''
        self.ventana_album.show()
        self.ventana_album.mostrar_album(self.logica.darAlbumPorId(indice_album))
        self.ventana_album.mostrar_canciones(self.logica.darCancionesDeAlbum(indice_album))

    def mostrar_ventana_lista_canciones(self):
        '''
        Método para mostrar la ventana de la lista de canciones
        '''
        self.ventana_lista_canciones.show()
        self.ventana_lista_canciones.mostrar_canciones(self.logica.darCanciones())

    def mostrar_ventana_cancion(self, nueva=False, id_album=-1, id_cancion=-1):
        '''
        Método para mostrar la ventana de una canción.
        Si el parámetro nueva es True, se crea para añadir una nueva canción.
        El parámetro id_album indica si la ventana se despliega desde un album.
        El parámetro id_cancion indica que canción existente se debe mostrar
        '''
        self.ventana_cancion.id_album = id_album
        if not nueva:
            cancion = self.logica.darCancionPorId(self.ventana_cancion.cancion_actual["id"] if id_cancion==-1 else id_cancion)
            self.ventana_cancion.mostrar_cancion(cancion)
            self.ventana_cancion.mostrar_interpretes(cancion["interpretes"])
        else:
            self.ventana_cancion.mostrar_cancion()
        self.ventana_cancion.show()

    def mostrar_ventana_buscar(self):
        '''
        Método para desplegar la ventana de búsquedas
        '''
        self.ventana_buscar.show()

    def guardar_album(self, n_album, nuevo_album):
        '''
        Método para guardar un album
        '''
        self.logica.editarAlbum(n_album, nuevo_album["titulo"], nuevo_album["ano"], nuevo_album["descripcion"], nuevo_album["medio"])

    def guardar_cancion(self, nueva_cancion, interpretes):
        '''
        Método para editar una canción
        '''
        res = self.logica.editarCancion(nueva_cancion["id"], nueva_cancion["titulo"], nueva_cancion["minutos"], nueva_cancion["segundos"], nueva_cancion["compositor"], interpretes)

    def eliminar_album(self, id_album):
        '''
        Método para eliminar un album
        '''
        self.logica.eliminarAlbum(id_album)
        self.ventana_lista_album.mostrar_albums(self.logica.darAlbumes())

    def eliminar_cancion(self, id_cancion):
        '''
        Método para eliminar una canción
        '''
        self.ventana_cancion.hide()
        self.logica.eliminarCancion(id_cancion)
        self.ventana_lista_canciones.mostrar_canciones(self.logica.darCanciones())

    def eliminar_interprete(self, id_interprete):
        '''
        Método para eliminar un intérprete
        '''
        self.logica.eliminarInterprete(id_interprete)

    def crear_album(self, nuevo_album):
        '''
        Método para crear un album
        '''
        self.logica.agregarAlbum(nuevo_album["titulo"], nuevo_album["ano"], nuevo_album["descripcion"], nuevo_album["medio"])
        self.ventana_lista_album.mostrar_albums(self.logica.darAlbumes())


    def crear_cancion(self, nueva_cancion, interpretes, id_album=-1):
        '''
        Método para crear una nueva canción. 
        El parámetro id_album indica si la canción está o no asociada a un album
        '''
        if id_album == -1:
            self.logica.agregarCancion(nueva_cancion["titulo"],nueva_cancion["minutos"], nueva_cancion["segundos"], nueva_cancion["compositor"], id_album, interpretes)
        else:
            self.logica.agregarCancion(nueva_cancion["titulo"],nueva_cancion["minutos"], nueva_cancion["segundos"], nueva_cancion["compositor"], id_album, interpretes)

    def mostrar_resultados_albumes(self, nombre_album):
        '''
        Método para mostrar los resultados de búsqueda de albumes por nombre
        '''
        albumes = self.logica.buscarAlbumesPorTitulo(nombre_album)
        self.ventana_buscar.mostrar_resultados_albumes(albumes)

    def mostrar_resultados_canciones(self, nombre_cancion):
        '''
        Método para mostrar los resultados de búsqueda de canciones por nombre
        '''
        canciones = self.logica.buscarCancionesPorTitulo(nombre_cancion)
        self.ventana_buscar.mostrar_resultados_canciones(canciones)

    def mostrar_resultados_interpretes(self, nombre_interprete):
        '''
        Método para mostrar los resultados de búsqueda de intérpretes por nombre
        '''
        interpretes = self.logica.buscarInterpretesPorNombre(nombre_interprete)
        self.ventana_buscar.mostrar_resultados_interpretes(interpretes)

    def agregar_interprete(self,  id_cancion, nombre, texto_curiosidades):
        '''
        Método para agregar un nuevo intérprete en una canción
        '''
        res = self.logica.agregarInterprete(nombre, texto_curiosidades, id_cancion)
        self.ventana_cancion.mostrar_cancion(self.logica.darCancionPorId(id_cancion))

    def asociar_cancion(self, id_album, id_cancion):
        '''
        Método para asociar una canción a un album
        '''
        self.logica.asociarCancion(id_cancion, id_album)
        self.ventana_album.mostrar_album(self.logica.darAlbumPorId(id_album))
        self.ventana_album.mostrar_canciones(self.logica.darCancionesDeAlbum(id_album))

    def dar_canciones(self):
        '''
        Método para dar todas las canciones
        '''
        return self.logica.darCanciones()
    
    def dar_medios(self):
        '''
        Método para obtener los valores de la enumeración medios del mundo
        '''
        return self.logica.darMedios()

    def dar_interpretes(self):
        '''
        Método para dar todos los intérpretes
        '''
        return self.logica.darInterpretes()
