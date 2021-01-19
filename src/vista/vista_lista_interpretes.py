 
from PyQt5.QtWidgets import QDialog, QScrollArea, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
        
class Ventana_Lista_Interpretes(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - intérpretes'
        self.left = 80
        self.top = 80
        self.width = 500
        self.height = 400
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_lista_interpretes = QVBoxLayout()
        self.setLayout(self.distr_lista_interpretes)
        
     
        
        self.lista_interpretes = QScrollArea()
        self.lista_interpretes.setWidgetResizable(True)
        self.caja_interpretes = QGroupBox()
        layout_interpretes = QGridLayout()
        self.caja_interpretes.setLayout(layout_interpretes)
        self.lista_interpretes.setWidget(self.caja_interpretes)

        etiqueta_intepretes = QLabel("Intérpretes")
        etiqueta_intepretes.setFont(QFont("Times",weight=QFont.Bold)) 
        layout_interpretes.addWidget(etiqueta_intepretes,0,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        etiqueta_acciones = QLabel("Acciones")
        etiqueta_acciones.setFont(QFont("Times",weight=QFont.Bold)) 
        layout_interpretes.addWidget(etiqueta_acciones,0,1,1,2, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar)

        self.boton_nuevo = QPushButton("Nuevo")
        self.boton_nuevo.clicked.connect(self.mostrar_dialogo_nuevo_interprete)

        self.boton_canciones = QPushButton("Ver Canciones")
        self.boton_canciones.clicked.connect(self.ver_canciones)

        self.boton_albumes = QPushButton("Ver Álbumes")
        self.boton_albumes.clicked.connect(self.ver_albumes)
        
        self.distr_lista_interpretes.addWidget(self.lista_interpretes)
        
        self.widget_botones = QWidget()
        self.widget_botones.setLayout(QHBoxLayout())
        self.distr_lista_interpretes.addWidget(self.widget_botones)

        self.widget_botones.layout().addWidget(self.boton_buscar)
        self.widget_botones.layout().addWidget(self.boton_nuevo)
        self.widget_botones.layout().addWidget(self.boton_canciones)
        self.widget_botones.layout().addWidget(self.boton_albumes)


    def limpiar_interpretes(self):
        while self.caja_interpretes.layout().count() > 2:
            child = self.caja_interpretes.layout().takeAt(2)
            if child.widget():
                child.widget().deleteLater()

    def mostrar_interpretes(self, interpretes):
        self.limpiar_interpretes()
        fila = 1
        for interprete in interpretes:
            campo_nombre = QLineEdit(interprete["nombre"])
            campo_nombre.setFixedWidth(300)
            campo_nombre.setReadOnly(True)
            self.caja_interpretes.layout().addWidget(campo_nombre,fila,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            boton_ver = QPushButton("Ver")
            boton_ver.setFixedWidth(50)
            boton_ver.clicked.connect(lambda estado, x=interprete["id"]: self.ver_interprete(x))
            self.caja_interpretes.layout().addWidget(boton_ver,fila,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedWidth(50)
            boton_borrar.clicked.connect(lambda estado, x=interprete["id"]: self.interfaz.eliminar_interprete(x))
            self.caja_interpretes.layout().addWidget(boton_borrar,fila,2, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            fila+=1

    def ver_interprete(self, interprete):
        self.interfaz.mostrar_ventana_interprete(interprete)
        self.hide()

    def mostrar_dialogo_nuevo_interprete(self):
        self.dialogo_nuevo_interprete = QDialog(self)

        layout = QGridLayout()
        self.dialogo_nuevo_interprete.setLayout(layout)
        self.dialogo_nuevo_interprete.setFixedSize(400,100)

        lab1 = QLabel("Nombre")
        txt1 = QLineEdit()
        layout.addWidget(lab1,0,0)
        layout.addWidget(txt1,0,1)
        
        widget_botones = QWidget()
        widget_botones.setFixedHeight(50)
        widget_botones.setLayout(QGridLayout())

        butAceptar = QPushButton("Aceptar")
        butCancelar = QPushButton("Cancelar")

        widget_botones.layout().addWidget(butAceptar,0,0)
        widget_botones.layout().addWidget(butCancelar,0,1)

        layout.addWidget(widget_botones, 4,0,1,2)

        butAceptar.clicked.connect(lambda: self.crear_interprete(txt1.text()))
        butCancelar.clicked.connect(lambda: self.dialogo_nuevo_interprete.close())

        self.dialogo_nuevo_interprete.setWindowTitle("Añadir nuevo interprete")
        self.dialogo_nuevo_interprete.exec_()

    def crear_interprete(self, nuevo_interprete):
        self.interfaz.crear_interprete(nuevo_interprete)
        self.dialogo_nuevo_interprete.close()

    def ver_canciones(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()   

    def ver_albumes(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_albums()   

    def buscar(self):
        self.hide()
        self.interfaz.mostrar_ventana_buscar()
