from PyQt5.QtWidgets import QScrollArea, QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QComboBox
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
        self.height = 450
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_album = QVBoxLayout()
        self.setLayout(self.distr_album)

        #Datos del album (editables)

        self.caja_album = QGroupBox()
        self.caja_album.setLayout(QHBoxLayout())

        self.caja_datos = QGroupBox()
        layout_datos = QGridLayout()
        self.caja_datos.setLayout(layout_datos)
    
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
        self.boton_adicionar.clicked.connect(self.mostrar_dialogo_nueva_cancion)
        self.boton_adicionar = QPushButton("Canción existente")
        layout_botones.addWidget(self.boton_adicionar)

        self.caja_album.layout().addWidget(self.caja_datos)
        self.caja_album.layout().addWidget(self.caja_botones)

        self.caja_titulos = QGroupBox()
        layout_titulos = QGridLayout()
        self.caja_titulos.setLayout(layout_titulos)

        self.boton_albums = QPushButton("Ver lista de albums")
        self.boton_albums.clicked.connect(self.ver_albums)

        self.lista_canciones = QScrollArea()
        self.lista_canciones.setWidgetResizable(True)
        self.caja_canciones = QWidget()
        self.caja_canciones.setLayout(QGridLayout())
        self.lista_canciones.setWidget(self.caja_canciones)

        self.titulos_cancion = ["Título de la canción", "Intérpretes", "Duración", "Acciones"]
        for i in range(len(self.titulos_cancion)):
            etiqueta = QLabel(self.titulos_cancion[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            self.caja_canciones.layout().addWidget(etiqueta,0,i, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        self.distr_album.addWidget(self.caja_album)
        self.distr_album.addWidget(self.caja_titulos)
        self.distr_album.addWidget(self.lista_canciones)
        self.distr_album.addWidget(self.boton_albums)

    def mostrar_album(self, album):
        self.album_actual = album
        self.texto_album.setText(album["titulo"])
        self.texto_anio.setText(str(album["ano"]))
        self.texto_descripcion.setText(album["descripcion"])
        self.lista_medios.setCurrentIndex(self.interfaz.dar_medios().index(album["medio"].name))

    def limpiar_canciones(self):
        while self.caja_canciones.layout().count()>len(self.titulos_cancion):
            child = self.caja_canciones.layout().takeAt(len(self.titulos_cancion))
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
            
            self.botones.append(QPushButton("Quitar"))
            self.botones[i].clicked.connect(lambda estado, x=canciones[i]["id"]: self.interfaz.quitar_cancion_de_album(x))
            self.caja_canciones.layout().addWidget(self.botones[i],i+1,3)

    def guardar_album(self):
        album_modificado = {"titulo":self.texto_album.text(),"interpretes":self.texto_descripcion.text(), "medio":self.lista_medios.currentText(),"ano":self.texto_anio.text(),"descripcion":self.texto_descripcion.text()}
        self.interfaz.guardar_album(self.album_actual["id"], album_modificado)

    def eliminar_album(self):
        self.interfaz.eliminar_album(self.album_actual)
    

    def ver_albums(self):
        self.interfaz.mostrar_ventana_lista_albums()
        self.hide()

    def mostrar_dialogo_nueva_cancion(self):
        self.dialogo_nueva_cancion = QDialog(self)
        
        layout = QGridLayout()
        self.dialogo_nueva_cancion.setLayout(layout)

        lab1 = QLabel("Título")
        txt1 = QLineEdit()
        layout.addWidget(lab1,0,0)
        layout.addWidget(txt1,0,1,1,3)

        lab2 = QLabel("Duración")
        txt2_1 = QLineEdit(maxLength=2)
        txt2_2 = QLineEdit(maxLength=2)
        layout.addWidget(lab2,1,0)
        layout.addWidget(txt2_1,1,1)
        layout.addWidget(QLabel(":"), 1,2)
        layout.addWidget(txt2_2,1,3)

        lab3 = QLabel("Compositor")
        txt3 = QLineEdit()
        layout.addWidget(lab3,2,0)
        layout.addWidget(txt3,2,1,1,3)

        butAceptar = QPushButton("Aceptar")
        butCancelar = QPushButton("Cancelar")
        
        layout.addWidget(butAceptar,4,0)
        layout.addWidget(butCancelar,4,1)
        
        butAceptar.clicked.connect(lambda: self.crear_cancion( {"Titulo":txt1.text(),"Interpretes":"", "Minutos":txt2_1.text(),"Segundos":txt2_2.text(),"Compositor":txt3.text()}))
        butCancelar.clicked.connect(lambda: self.dialogo_nueva_cancion.close())

        self.dialogo_nueva_cancion.setWindowTitle("Añadir nueva canción")
        self.dialogo_nueva_cancion.exec_()
        self.dialogo_nueva_cancion.close()

    def crear_cancion(self, nueva_cancion):
        pass
