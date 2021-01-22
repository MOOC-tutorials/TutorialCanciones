
from PyQt5.QtWidgets import QScrollArea, QPlainTextEdit, QComboBox, QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class Ventana_Cancion(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - canción'
        self.left = 80
        self.top = 80
        self.width = 500
        self.height = 400
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_cancion = QVBoxLayout()
        self.setLayout(self.distr_cancion)
        
        self.caja_datos = QGroupBox()
        layout_datos = QGridLayout()
        self.caja_datos.setLayout(layout_datos)

        datos = ["Canción", "Duración", "Compositor"]
        for i in range(len(datos)):
            etiqueta = QLabel(datos[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            layout_datos.addWidget(etiqueta,i,0)

        self.texto_cancion = QLineEdit()
        layout_datos.addWidget(self.texto_cancion, 0, 1, 1, 3)

        self.texto_minutos = QLineEdit(maxLength=2)
        layout_datos.addWidget(self.texto_minutos, 1, 1)

        layout_datos.addWidget(QLabel(":"),1,2)

        self.texto_segundos = QLineEdit(maxLength=2)
        layout_datos.addWidget(self.texto_segundos, 1, 3)

        self.texto_compositor = QLineEdit()
        layout_datos.addWidget(self.texto_compositor, 2, 1, 1, 3)

        self.caja_botones = QWidget()
        layout_botones = QVBoxLayout()
        self.caja_botones.setLayout(layout_botones)

        self.boton_guardar = QPushButton("Guardar datos editados")
        self.boton_guardar.clicked.connect(lambda: self.interfaz.guardar_cancion(self.cancion_actual["id"], {"titulo":self.texto_cancion.text(), "minutos":self.texto_minutos.text(),"segundos":self.texto_segundos.text(),"compositor":self.texto_compositor.text()}))
        layout_botones.addWidget(self.boton_guardar)

        self.boton_adicionar = QPushButton("Adicionar intérprete")
        self.boton_adicionar.clicked.connect(self.mostrar_dialogo_crear_interprete)
        layout_botones.addWidget(self.boton_adicionar)

        self.boton_canciones = QPushButton("Ver lista de canciones")
        self.boton_canciones.clicked.connect(self.mostrar_lista_canciones)
        layout_botones.addWidget(self.boton_canciones)

        self.lista_interpretes = QScrollArea()
        self.lista_interpretes.setFixedHeight(200)
        self.lista_interpretes.setWidgetResizable(True)
        self.caja_interpretes = QWidget()
        self.caja_interpretes.setLayout(QGridLayout())
        self.lista_interpretes.setWidget(self.caja_interpretes)

        layout_datos.addWidget(self.caja_botones, 0, 4, 3, 1)

        etiqueta_interpretes = QLabel("Intérpretes")
        etiqueta_interpretes.setFont(QFont("Times",weight=QFont.Bold))
        etiqueta_interpretes.setAlignment(QtCore.Qt.AlignCenter)

        etiqueta_nombre_interprete = QLabel("Nombre")
        etiqueta_nombre_interprete.setFont(QFont("Times",weight=QFont.Bold))
        self.caja_interpretes.layout().addWidget(etiqueta_nombre_interprete, 0, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        etiqueta_acciones = QLabel("Acciones")
        etiqueta_acciones.setFont(QFont("Times",weight=QFont.Bold))
        self.caja_interpretes.layout().addWidget(etiqueta_acciones, 0, 1,  QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        self.distr_cancion.addWidget(self.caja_datos)
        self.distr_cancion.addWidget(etiqueta_interpretes,  QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.distr_cancion.addWidget(self.lista_interpretes)
        

    def limpiar_interpretes(self):
        while self.caja_interpretes.layout().count() > 2:
            child = self.caja_interpretes.layout().takeAt(2)
            if child.widget():
                child.widget().deleteLater()


    def mostrar_cancion(self, cancion, interpretes=[]):
        self.cancion_actual = cancion
        self.texto_cancion.setText(cancion["titulo"])
        self.texto_minutos.setText(str(cancion["minutos"]))
        self.texto_segundos.setText(str(cancion["segundos"]))
        self.texto_compositor.setText(cancion["compositor"])
        self.limpiar_interpretes()
        fila=1

        

        for interprete in cancion.get("interpretes",[]):
            campo_nombre = QLineEdit(interprete["nombre"])
            campo_nombre.setFixedWidth(300)
            campo_nombre.setReadOnly(True)

            widget_botones = QWidget()
            widget_botones.setLayout(QGridLayout())

            self.caja_interpretes.layout().addWidget(campo_nombre,fila,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            boton_ver = QPushButton("Ver")
            boton_ver.setFixedSize(50,25)
            boton_ver.clicked.connect(lambda estado, x=interprete["id"]: self.ver_interprete(x))
            widget_botones.layout().addWidget(boton_ver,fila,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedWidth(50)
            boton_borrar.setFixedSize(50,25)
            boton_borrar.clicked.connect(lambda estado, x=interprete["id"]: self.interfaz.eliminar_interprete(x))
            widget_botones.layout().addWidget(boton_borrar,fila,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            widget_botones.layout().setContentsMargins(0,0,0,0)
            
            self.caja_interpretes.layout().addWidget(widget_botones, fila, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            
            fila+=1
        self.caja_interpretes.layout().setRowStretch(fila, 1)

    def ver_canciones(self):
        self.interfaz.mostrar_ventana_lista_canciones()
        self.hide()

    def mostrar_dialogo_crear_interprete(self):
        self.dialogo_nuevo_interprete = QDialog(self)

        layout = QGridLayout()
        self.dialogo_nuevo_interprete.setLayout(layout)
        self.dialogo_nuevo_interprete.setFixedSize(400,300)

        lab1 = QLabel("Nombre:")
        txt1 = QLineEdit()
        layout.addWidget(lab1,0,0)
        layout.addWidget(txt1,0,1)
        
        lab2 = QLabel("Curiosidades:")
        txt2 = QPlainTextEdit()
        txt2.setFixedWidth(275)
        layout.addWidget(lab2, 1, 0, 1, 1, QtCore.Qt.AlignTop)
        layout.addWidget(txt2, 1, 1, 1, 4)

        widget_botones = QWidget()
        widget_botones.setFixedHeight(50)
        widget_botones.setLayout(QGridLayout())

        butAceptar = QPushButton("Aceptar")
        butCancelar = QPushButton("Cancelar")

        widget_botones.layout().addWidget(butAceptar,0,0)
        widget_botones.layout().addWidget(butCancelar,0,1)

        layout.addWidget(widget_botones, 4,0,1,2)

        butAceptar.clicked.connect(lambda: self.agregar_interprete(txt1.text(), txt2.toPlainText()))
        butCancelar.clicked.connect(lambda: self.dialogo_nuevo_interprete.close())

        self.dialogo_nuevo_interprete.setWindowTitle("Añadir nuevo interprete")
        self.dialogo_nuevo_interprete.exec_()

    def ver_interprete(self, id_interprete):
        self.interfaz.mostrar_ventana_interprete(id_interprete)
        self.hide()

    def agregar_interprete(self, nombre, texto_curiosidades):
        self.interfaz.agregar_interprete(self.cancion_actual['id'], nombre, texto_curiosidades)
        self.dialogo_nuevo_interprete.close()

    def mostrar_lista_canciones(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()