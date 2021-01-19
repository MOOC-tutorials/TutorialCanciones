from PyQt5.QtWidgets import QDialog, QScrollArea, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, Qt

class Ventana_Inicial(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - Búsqueda'
        self.left = 80
        self.top = 80
        self.width = 500
        self.height = 400
        #Inicializamos la ventana principal
        self.inicializar_ventana()

        #Asignamos el valor de la lógica
        #¿?
    
    def inicializar_ventana(self):
        #inicializamos la ventana
        self.setWindowTitle(self.title)
        self.setFixedSize( self.width, self.height)
        
        
        self.distr_caja_busquedas = QGridLayout()
        self.setLayout(self.distr_caja_busquedas)

        self.etiqueta_album = QLabel('Título del album')
        self.txt_album = QLineEdit()

        self.boton_buscar_album = QPushButton("Buscar")
        self.boton_buscar_album.clicked.connect(self.buscar_album)

        self.boton_ver_albumes = QPushButton("Ver todos")
        self.boton_ver_albumes.clicked.connect(self.ver_albumes)


        self.etiqueta_cancion = QLabel('Título de la canción')
        self.txt_cancion = QLineEdit()

        self.boton_buscar_cancion = QPushButton("Buscar")
        self.boton_buscar_cancion.clicked.connect(self.buscar_cancion)

        self.boton_ver_canciones = QPushButton("Ver todas")
        self.boton_ver_canciones.clicked.connect(self.ver_canciones)

        self.etiqueta_interprete = QLabel('Intérprete de la canción')
        self.txt_interprete = QLineEdit()

        self.boton_buscar_interprete = QPushButton("Buscar")
        self.boton_buscar_interprete.clicked.connect(self.buscar_interprete)

        self.boton_ver_interpretes = QPushButton("Ver todos")
        self.boton_ver_interpretes.clicked.connect(self.ver_interpretes)

        self.etiqueta_resultados = QLabel('Resultados')
        self.etiqueta_resultados.setFont(QFont("Times", weight=QFont.Bold))

        self.distr_caja_busquedas.addWidget(self.etiqueta_album, 0,0)
        self.distr_caja_busquedas.addWidget(self.txt_album, 0, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_album, 0, 2)
        self.distr_caja_busquedas.addWidget(self.boton_ver_albumes, 0, 3)

        self.distr_caja_busquedas.addWidget(self.etiqueta_cancion, 1,0)
        self.distr_caja_busquedas.addWidget(self.txt_cancion, 1, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_cancion, 1, 2)
        self.distr_caja_busquedas.addWidget(self.boton_ver_canciones, 1, 3)

        self.distr_caja_busquedas.addWidget(self.etiqueta_interprete, 2,0)
        self.distr_caja_busquedas.addWidget(self.txt_interprete, 2, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_interprete, 2, 2)
        self.distr_caja_busquedas.addWidget(self.boton_ver_interpretes, 2, 3)

        self.distr_caja_busquedas.addWidget(self.etiqueta_resultados, 3, 0, 1, 4)
        self.distr_caja_busquedas.setAlignment(self.etiqueta_resultados, QtCore.Qt.AlignCenter)

        self.tabla_resultados = QScrollArea()
        self.tabla_resultados.setFixedHeight(200)
        self.tabla_resultados.setWidgetResizable(True)
        self.widget_tabla_resultados = QWidget()
        self.widget_tabla_resultados.setLayout(QGridLayout())
        self.tabla_resultados.setWidget(self.widget_tabla_resultados)
        self.distr_caja_busquedas.addWidget(self.tabla_resultados, 4, 0, 1, 4)


    def buscar_album(self):
        self.interfaz.mostrar_resultados_albumes(self.txt_album.text())

    def limpiar_resultados(self):
        while self.widget_tabla_resultados.layout().count()>0:
            child = self.widget_tabla_resultados.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def mostrar_resultados_albumes(self, lista_albums):
        
        self.limpiar_resultados()

        etiqueta_titulo = QLabel("Título")
        etiqueta_titulo.setFixedSize(200,30)
        etiqueta_titulo.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_tabla_resultados.layout().addWidget(etiqueta_titulo, 0, 0, 1, 2)
        self.widget_tabla_resultados.layout().setAlignment(etiqueta_titulo, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)  

        fila = 1
        for album in lista_albums:
            etiqueta_nombre = QLabel(album["titulo"])
            etiqueta_nombre.setFixedSize(200,30)
            self.widget_tabla_resultados.layout().addWidget(etiqueta_nombre, fila, 0, 1, 2)  
            self.widget_tabla_resultados.layout().setAlignment(etiqueta_nombre, QtCore.Qt.AlignTop)
            boton_ver = QPushButton("Ver")
            boton_ver.clicked.connect(lambda estado, id=album["id"]: self.ver_album(id))
            boton_ver.setFixedSize(40,30)
            self.widget_tabla_resultados.layout().addWidget(boton_ver, fila, 1)   
            self.widget_tabla_resultados.layout().setAlignment(boton_ver, QtCore.Qt.AlignTop)
            fila+=1
    
    def mostrar_resultados_canciones(self, lista_canciones):
        
        self.limpiar_resultados()

        etiqueta_titulo = QLabel("Título")
        etiqueta_titulo.setFixedSize(200,30)
        etiqueta_titulo.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_tabla_resultados.layout().addWidget(etiqueta_titulo, 0, 0, 1, 2)
        self.widget_tabla_resultados.layout().setAlignment(etiqueta_titulo, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)  

        fila = 1
        for cancion in lista_canciones:
            etiqueta_nombre = QLabel(cancion["titulo"])
            etiqueta_nombre.setFixedSize(200,30)
            self.widget_tabla_resultados.layout().addWidget(etiqueta_nombre, fila, 0, 1, 2)  
            self.widget_tabla_resultados.layout().setAlignment(etiqueta_nombre, QtCore.Qt.AlignTop)
            boton_ver = QPushButton("Ver")
            boton_ver.clicked.connect(lambda estado, id=cancion["id"]: self.ver_cancion(id))
            boton_ver.setFixedSize(40,30)
            self.widget_tabla_resultados.layout().addWidget(boton_ver, fila, 1)   
            self.widget_tabla_resultados.layout().setAlignment(boton_ver, QtCore.Qt.AlignTop)
            fila+=1
    
    def mostrar_resultados_interpretes(self, lista_interpretes):
        
        self.limpiar_resultados()

        etiqueta_titulo = QLabel("Nombre")
        etiqueta_titulo.setFixedSize(200,30)
        etiqueta_titulo.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_tabla_resultados.layout().addWidget(etiqueta_titulo, 0, 0, 1, 2)
        self.widget_tabla_resultados.layout().setAlignment(etiqueta_titulo, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)  

        fila = 1
        for interprete in lista_interpretes:
            etiqueta_nombre = QLabel(interprete["nombre"])
            etiqueta_nombre.setFixedSize(200,30)
            self.widget_tabla_resultados.layout().addWidget(etiqueta_nombre, fila, 0, 1, 2)  
            self.widget_tabla_resultados.layout().setAlignment(etiqueta_nombre, QtCore.Qt.AlignTop)
            boton_ver = QPushButton("Ver")
            boton_ver.clicked.connect(lambda estado, id=interprete["id"]: self.ver_interprete(id))
            boton_ver.setFixedSize(40,30)
            self.widget_tabla_resultados.layout().addWidget(boton_ver, fila, 1)   
            self.widget_tabla_resultados.layout().setAlignment(boton_ver, QtCore.Qt.AlignTop)
            fila+=1


    def ver_albumes(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_albums()

    def ver_album(self, indice_album):
        self.hide()
        self.interfaz.mostrar_ventana_album(indice_album)

    def buscar_cancion(self):
        self.interfaz.mostrar_resultados_canciones(self.txt_cancion.text())

    def ver_canciones(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()

    def ver_cancion(self, indice_cancion):
        self.hide()
        self.interfaz.mostrar_ventana_cancion(indice_cancion)
     
    def buscar_interprete(self):
        self.interfaz.mostrar_resultados_interpretes(self.txt_interprete.text())


    def ver_interpretes(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_interpretes()

    def ver_interprete(self, indice_interprete):
        self.hide()
        self.interfaz.mostrar_ventana_interprete(indice_interprete)
 
