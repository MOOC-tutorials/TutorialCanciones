from PyQt5.QtWidgets import QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class Ventana_Album(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - album'
        self.left = 80
        self.top = 80
        self.width = 500
        self.height = 150
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.distr_album = QVBoxLayout()
        self.setLayout(self.distr_album)

        #Datos del album (editables)

        self.caja_album = QGroupBox()
        self.caja_album.setLayout(QHBoxLayout())

        self.caja_datos = QGroupBox()
        layout_datos = QGridLayout()
        self.caja_datos.setLayout(layout_datos)

        datos = ["Album", "Año de producción", "Descripción", "Medio"]
        for i in range(len(datos)):
            etiqueta = QLabel(datos[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            layout_datos.addWidget(etiqueta,i,0)

       
        self.texto_album = QLineEdit()
        layout_datos.addWidget(self.texto_album, 0, 1)

        self.texto_anio = QLineEdit()
        layout_datos.addWidget(self.texto_anio, 1, 1)

        self.texto_descripcion = QLineEdit()
        layout_datos.addWidget(self.texto_descripcion, 2, 1)

        self.lista_medios = QComboBox()
        self.lista_medios.addItems(self.interfaz.dar_medios())
        layout_datos.addWidget(self.lista_medios, 3, 1)

        self.caja_botones = QGroupBox()
        layout_botones = QVBoxLayout()
        self.caja_botones.setLayout(layout_botones)

        self.boton_guardar = QPushButton("Guardar datos editados")
        self.boton_guardar.clicked.connect(self.guardar_album)
        layout_botones.addWidget(self.boton_guardar)

        self.boton_borrar = QPushButton("Borrar")
        self.boton_borrar.clicked.connect(self.eliminar_album)
        layout_botones.addWidget(self.boton_borrar)
        
        self.boton_adicionar = QPushButton("Nueva canción")
        layout_botones.addWidget(self.boton_adicionar)
        self.boton_adicionar = QPushButton("canción existente")
        layout_botones.addWidget(self.boton_adicionar)

        self.caja_album.layout().addWidget(self.caja_datos)
        self.caja_album.layout().addWidget(self.caja_botones)

        self.caja_titulos = QGroupBox()
        layout_titulos = QGridLayout()
        self.caja_titulos.setLayout(layout_titulos)

        titulos = ["Título de la canción", "Intérpretes", "Duración", "Acciones"]
        for i in range(len(titulos)):
            etiqueta = QLabel(titulos[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            layout_titulos.addWidget(etiqueta,0,i)

        self.boton_albums = QPushButton("Ver Álbums")
        self.boton_albums.clicked.connect(self.ver_albums)

        self.caja_canciones = QGroupBox()
        layout_canciones = QGridLayout()
        self.caja_canciones.setLayout(layout_canciones)

        self.distr_album.addWidget(self.caja_album)
        self.distr_album.addWidget(self.caja_titulos)
        self.distr_album.addWidget(self.caja_canciones)
        self.distr_album.addWidget(self.boton_albums)

    def mostrar_album(self, n_album, album):
        self.album_actual = n_album
        self.texto_album.setText(album["titulo"])
        self.texto_anio.setText(str(album["ano"]))
        self.texto_descripcion.setText(album["descripcion"])
        self.lista_medios.setCurrentIndex(self.interfaz.dar_medios().index(album["medio"].name))

    def limpiar_canciones(self):
        while self.caja_canciones.layout().count():
            child = self.caja_canciones.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def mostrar_canciones(self, canciones):
        self.limpiar_canciones()
        self.botones = []
        for i in range(len(canciones)):
            texto_titulo = QLineEdit(canciones[i]["Titulo"])
            texto_titulo.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_titulo,i+1,0)

            texto_interpretes = QLineEdit(canciones[i]["Intérpretes"])
            texto_interpretes.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_interpretes,i+1,1)
            
            texto_duracion = QLineEdit(canciones[i]["Duracion"])
            texto_duracion.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_duracion,i+1,2)
            
            self.botones.append(QPushButton("Ver"))
            self.botones[i].clicked.connect(lambda estado, x=i: self.ver_cancion(x))
            self.caja_canciones.layout().addWidget(self.botones[i],i+1,3)

    def guardar_album(self):
        album_modificado = {"Titulo":self.texto_album.text(),"Intérpretes":self.texto_descripcion.text(), "Medio":self.lista_medios.currentText(),"Anio":self.texto_anio.text(),"Descripcion":self.texto_descripcion.text()}
        self.interfaz.guardar_album(self.album_actual, album_modificado)

    def eliminar_album(self):
        self.interfaz.eliminar_album(self.album_actual)
    
    def ver_cancion(self, n_boton):
        self.interfaz.mostrar_ventana_cancion(n_boton)
        self.hide()

    def ver_albums(self):
        self.interfaz.mostrar_ventana_lista_albums()
        self.hide()

   