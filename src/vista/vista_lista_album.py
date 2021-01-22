from PyQt5.QtWidgets import QScrollArea, QDialog, QComboBox, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class Ventana_Lista_Album(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - albums'
        self.left = 80
        self.top = 80
        self.width = 500
        self.height = 450
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_lista_canciones = QVBoxLayout()
        self.setLayout(self.distr_lista_canciones)
        
        self.lista_albums = QScrollArea()
        self.lista_albums.setWidgetResizable(True)
        self.caja_albums = QWidget()
        self.caja_albums.setLayout(QGridLayout())
        self.lista_albums.setWidget(self.caja_albums)

        self.titulos = ["Titulo del album", "Intérpretes", "Medio", "Acciones"]
        
        for i in range(len(self.titulos)):
            etiqueta_titulo = QLabel(self.titulos[i])
            etiqueta_titulo.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)
            self.caja_albums.layout().addWidget(etiqueta_titulo,0,i, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)


        self.caja_botones = QGroupBox()
        layout_botones = QHBoxLayout()
        self.caja_botones.setLayout(layout_botones)


        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar)

        self.boton_nuevo = QPushButton("Nuevo")
        self.boton_nuevo.clicked.connect(self.nuevo_album)

        self.boton_canciones = QPushButton("Ver Canciones")
        self.boton_canciones.clicked.connect(self.ver_canciones)


        layout_botones.addWidget(self.boton_buscar)
        layout_botones.addWidget(self.boton_nuevo)
        layout_botones.addWidget(self.boton_canciones)

        self.distr_lista_canciones.addWidget(self.lista_albums)
        self.distr_lista_canciones.addWidget(self.caja_botones)
    
    def mostrar_albums(self, albumes):
        self.limpiar_albums()

        i = 1
        for album in albumes:
            texto_titulo = QLineEdit(album["titulo"])
            texto_titulo.setReadOnly(True)
            self.caja_albums.layout().addWidget(texto_titulo,i,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            texto_interpretes = QLineEdit(";".join(album.get("interpretes",[])))
            texto_interpretes.setReadOnly(True)
            self.caja_albums.layout().addWidget(texto_interpretes,i,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            texto_medio = QLineEdit(album["medio"].name)
            texto_medio.setReadOnly(True)
            self.caja_albums.layout().addWidget(texto_medio,i,2, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            
            widget_botones = QWidget()
            widget_botones.setLayout(QGridLayout())

            boton_ver = QPushButton("Ver")
            boton_ver.setFixedSize(50,25)
            boton_ver.clicked.connect(lambda estado, x=album["id"]: self.ver_album(x))
            widget_botones.layout().addWidget(boton_ver,0,0)

            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedSize(50,25)
            boton_borrar.clicked.connect(lambda estado, x=album["id"]: self.interfaz.eliminar_album(x))
            widget_botones.layout().addWidget(boton_borrar,0,1 )

            widget_botones.layout().setContentsMargins(0,0,0,0)

            self.caja_albums.layout().addWidget(widget_botones, i, 3, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            i+=1
        self.caja_albums.layout().setRowStretch(i, 1)

    def limpiar_albums(self):
        while self.caja_albums.layout().count() > len(self.titulos) :
            child = self.caja_albums.layout().takeAt(len(self.titulos))
            if child.widget():
                child.widget().deleteLater()

    def ver_album(self, n_album):
        self.hide()
        self.interfaz.mostrar_ventana_album(n_album)
    
    def buscar(self):
        self.hide()
        self.interfaz.mostrar_ventana_buscar()

    def nuevo_album(self, nuevo_album):
        self.dialogo_nuevo_album = QDialog(self)
        
        layout = QGridLayout()
        self.dialogo_nuevo_album.setLayout(layout)

        lab1 = QLabel("Título")
        txt1 = QLineEdit()
        layout.addWidget(lab1,0,0)
        layout.addWidget(txt1,0,1)

        lab2 = QLabel("Anio")
        txt2 = QLineEdit()
        layout.addWidget(lab2,1,0)
        layout.addWidget(txt2,1,1)

        lab3 = QLabel("Descripcion")
        txt3 = QLineEdit()
        layout.addWidget(lab3,2,0)
        layout.addWidget(txt3,2,1)

        lab4 = QLabel("Medio")
        combo4 = QComboBox()
        combo4.addItems(self.interfaz.dar_medios())
        layout.addWidget(lab4,3,0)
        layout.addWidget(combo4,3,1)

        butAceptar = QPushButton("Aceptar")
        butCancelar = QPushButton("Cancelar")
        
        layout.addWidget(butAceptar,4,0)
        layout.addWidget(butCancelar,4,1)
        
        butAceptar.clicked.connect(lambda: self.crear_album( {"titulo":txt1.text(),"interpretes":"", "medio":combo4.currentText(),"ano":txt2.text(),"descripcion":txt3.text()}))
        butCancelar.clicked.connect(lambda: self.dialogo_nuevo_album.close())

        self.dialogo_nuevo_album.setWindowTitle("Añadir nuevo album")
        self.dialogo_nuevo_album.exec_()

    def crear_album(self, nuevo_album):
        self.interfaz.crear_album(nuevo_album)
        self.dialogo_nuevo_album.close()

    def ver_canciones(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()   

