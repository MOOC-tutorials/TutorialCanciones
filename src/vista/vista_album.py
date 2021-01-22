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
    
        etiqueta_titulo = QLabel("Título")
        etiqueta_titulo.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_titulo, 0, 0)

        etiqueta_ano = QLabel("Año")
        etiqueta_ano.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_ano, 1, 0)

        etiqueta_descripcion = QLabel("Descripción")
        etiqueta_descripcion.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_descripcion, 2, 0)

        etiqueta_medio = QLabel("Medio")
        etiqueta_medio.setFont(QFont("Times",weight=QFont.Bold))      
        layout_datos.addWidget(etiqueta_medio, 3, 0)

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
        
        self.boton_adicionar_nueva_cancion = QPushButton("Agregar nueva canción")
        layout_botones.addWidget(self.boton_adicionar_nueva_cancion)
        self.boton_adicionar_nueva_cancion.clicked.connect(self.crear_cancion)
        self.boton_adicionar_cancion_existente = QPushButton("Agregar canción existente")
        self.boton_adicionar_cancion_existente.clicked.connect(self.mostrar_dialogo_agregar_cancion)
        layout_botones.addWidget(self.boton_adicionar_cancion_existente)

        self.caja_album.layout().addWidget(self.caja_datos)
        self.caja_album.layout().addWidget(self.caja_botones)

        self.etiqueta_canciones = QLabel("Canciones")
        self.etiqueta_canciones.setFont(QFont("Times",weight=QFont.Bold))
        self.etiqueta_canciones.setAlignment(QtCore.Qt.AlignCenter)

        self.boton_albums = QPushButton("Ver lista de albums")
        self.boton_albums.clicked.connect(self.ver_albums)

        self.lista_canciones = QScrollArea()
        self.lista_canciones.setWidgetResizable(True)
        self.caja_canciones = QWidget()
        self.caja_canciones.setLayout(QGridLayout())
        self.lista_canciones.setWidget(self.caja_canciones)

        self.titulos_cancion = ["Título de la canción", "Compositor", "Duración", "Acciones"]
        for i in range(len(self.titulos_cancion)):
            etiqueta = QLabel(self.titulos_cancion[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            self.caja_canciones.layout().addWidget(etiqueta,0,i, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        self.distr_album.addWidget(self.caja_album)
        self.distr_album.addWidget(self.etiqueta_canciones)
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
        fila = 1
        for cancion in canciones:
            print(cancion)
            texto_titulo = QLineEdit(cancion["titulo"])
            texto_titulo.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_titulo,fila,0)

            texto_interpretes = QLineEdit(cancion["compositor"])
            texto_interpretes.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_interpretes,fila,1)
            
            texto_duracion = QLineEdit("{}:{}".format(cancion["minutos"],cancion["segundos"]))
            texto_duracion.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_duracion,fila,2)
            
            boton_quitar = QPushButton("Quitar")
            boton_quitar.clicked.connect(lambda estado, x=cancion: self.interfaz.quitar_cancion_de_album(x))
            self.caja_canciones.layout().addWidget(boton_quitar,fila,3)
            fila+=1

        self.caja_canciones.layout().setRowStretch(fila, 1)

    def guardar_album(self):
        album_modificado = {"titulo":self.texto_album.text(),"interpretes":self.texto_descripcion.text(), "medio":self.lista_medios.currentText(),"ano":self.texto_anio.text(),"descripcion":self.texto_descripcion.text()}
        self.interfaz.guardar_album(self.album_actual["id"], album_modificado)

    def eliminar_album(self):
        self.interfaz.eliminar_album(self.album_actual)
    

    def ver_albums(self):
        self.interfaz.mostrar_ventana_lista_albums()
        self.hide()

    def crear_cancion(self, nueva_cancion):
        self.interfaz.crear_cancion(nueva_cancion, self.album_actual["id"])

    def mostrar_dialogo_agregar_cancion(self):
        self.dialogo_agregar_cancion = QDialog(self)
        
        layout = QGridLayout()
        self.dialogo_agregar_cancion.setLayout(layout)

        lab1 = QLabel("Canciones")
        layout.addWidget(lab1,0,0)


        lista_canciones = QComboBox()
        for cancion in self.interfaz.dar_canciones():
            print(cancion)
            lista_canciones.addItem("{}".format(cancion["titulo"]), cancion["id"] )
            print(cancion["id"])
        layout.addWidget(lista_canciones,1,0)

        butAceptar = QPushButton("Agregar")
        butCancelar = QPushButton("Cancelar")
        
        caja_botones = QWidget()
        caja_botones.setLayout(QGridLayout())

        caja_botones.layout().addWidget(butAceptar,0,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        caja_botones.layout().addWidget(butCancelar,0,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        
        layout.addWidget(caja_botones, 3, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter )

        butAceptar.clicked.connect(lambda: self.asociar_cancion_a_album( lista_canciones.currentData()))
        butCancelar.clicked.connect(lambda: self.dialogo_agregar_cancion.close())

        self.dialogo_agregar_cancion.setWindowTitle("Añadir nueva canción")
        self.dialogo_agregar_cancion.exec_()
        self.dialogo_agregar_cancion.close()
    
    def asociar_cancion_a_album(self, id_cancion):
        self.interfaz.asociar_cancion(self.album_actual["id"], id_cancion)
        self.dialogo_agregar_cancion.close()
        
    def crear_cancion(self):
        self.interfaz.mostrar_ventana_cancion(nueva=True, album=self.album_actual["id"])
