from PyQt5.QtWidgets import QDialog, QPlainTextEdit, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class Ventana_Interprete(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - intérprete'
        self.left = 80
        self.top = 80
        self.width = 500
        self.height = 350
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_interprete = QVBoxLayout()
        self.setLayout(self.distr_interprete)
        
        self.caja_datos = QGroupBox()
        layout_datos = QGridLayout()
        self.caja_datos.setLayout(layout_datos)

        etiqueta_interprete = QLabel("Nombre")
        etiqueta_interprete.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_interprete, 0, 0)
        self.texto_interprete = QLineEdit()
        layout_datos.addWidget(self.texto_interprete, 0, 1)

        etiqueta_curiosidades = QLabel("Curiosidades")
        etiqueta_curiosidades.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_curiosidades, 1, 0, QtCore.Qt.AlignTop)
        self.texto_curiosidades = QPlainTextEdit()
        layout_datos.addWidget(self.texto_curiosidades, 1, 1)

        self.caja_botones = QWidget()
        layout_botones = QHBoxLayout()
        self.caja_botones.setLayout(layout_botones)

        self.boton_volver = QPushButton("Ver cancion")
        self.boton_volver.clicked.connect(self.volver_atras)
        layout_botones.addWidget(self.boton_volver)

        self.boton_guardar = QPushButton("Guardar datos editados")
        self.boton_guardar.clicked.connect(lambda: self.interfaz.guardar_interprete(self.interprete_actual["id"], self.texto_interprete.text()))
        layout_botones.addWidget(self.boton_guardar)


        self.boton_borrar = QPushButton("Borrar")
        self.boton_borrar.clicked.connect(lambda : self.interfaz.eliminar_interprete(self.interprete_actual["id"]))
        layout_botones.addWidget(self.boton_borrar)

        self.distr_interprete.addWidget(self.caja_datos)
        self.distr_interprete.addWidget(self.caja_botones)

    def mostrar_interprete(self, interprete):
        self.interprete_actual = interprete
        self.texto_interprete.setText(interprete["nombre"])
        self.texto_curiosidades.setPlainText(interprete["texto_curiosidades"])

    def volver_atras(self):
        self.hide()
        self.interfaz.mostrar_ventana_cancion()
