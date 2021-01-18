from PyQt5.QtWidgets import QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class Ventana_Inicial(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - Búsqueda'
        self.left = 80
        self.top = 80
        self.width = 500
        self.height = 150
        #Inicializamos la ventana principal
        self.inicializar_ventana()

        #Asignamos el valor de la lógica
        #¿?
    
    def inicializar_ventana(self):
        #inicializamos la ventana
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        
        self.distr_caja_busquedas = QGridLayout()
        self.setLayout(self.distr_caja_busquedas)

        self.etiqueta_album = QLabel('Título del album')
        self.txt_album = QLineEdit()
        self.boton_buscar_album = QPushButton("Buscar")
        self.boton_buscar_album.clicked.connect(self.buscar_album)

        self.etiqueta_cancion = QLabel('Título de la canción')
        self.txt_cancion = QLineEdit()
        self.boton_buscar_cancion = QPushButton("Buscar")
        self.boton_buscar_cancion.clicked.connect(self.buscar_cancion)

        self.etiqueta_interprete = QLabel('Intérprete de la canción')
        self.txt_interprete = QLineEdit()
        self.boton_buscar_interprete = QPushButton("Buscar")
        self.boton_buscar_interprete.clicked.connect(self.buscar_interprete)

        self.distr_caja_busquedas.addWidget(self.etiqueta_album, 0,0)
        self.distr_caja_busquedas.addWidget(self.txt_album, 0, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_album, 0, 2)

        self.distr_caja_busquedas.addWidget(self.etiqueta_cancion, 1,0)
        self.distr_caja_busquedas.addWidget(self.txt_cancion, 1, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_cancion, 1, 2)

        self.distr_caja_busquedas.addWidget(self.etiqueta_interprete, 2,0)
        self.distr_caja_busquedas.addWidget(self.txt_interprete, 2, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_interprete, 2, 2)


    def buscar_album(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_albums()

    def buscar_cancion(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()
     
    def buscar_interprete(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_interpretes()

 
