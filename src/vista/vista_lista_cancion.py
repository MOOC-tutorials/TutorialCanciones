
from PyQt5.QtWidgets import QScrollArea, QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

class Ventana_Lista_Canciones(QWidget):

    def __init__(self, app):
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - canciones'
        self.left = 80
        self.top = 80
        self.width = 550
        self.height = 300
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_album = QVBoxLayout()
        self.setLayout(self.distr_album)

        self.caja_canciones = QScrollArea()
        self.caja_canciones.setFixedHeight(225)
        self.caja_canciones.setWidgetResizable(True)
        layout_canciones = QGridLayout()
        self.caja_canciones.setLayout(layout_canciones)

        self.titulos = ["Título de la canción", "Intérpretes", "Duración", "Acciones"]
        for i in range(len(self.titulos)):
            etiqueta = QLabel(self.titulos[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            layout_canciones.addWidget(etiqueta,0,i)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar)

        self.boton_nuevo = QPushButton("Nuevo")
        self.boton_nuevo.clicked.connect(self.mostrar_dialogo_nueva_cancion)

        self.boton_interpretes = QPushButton("Ver Intérpretes")
        self.boton_interpretes.clicked.connect(self.ver_interpretes)

        self.boton_albumes = QPushButton("Ver Álbumes")
        self.boton_albumes.clicked.connect(self.ver_albumes)

        self.distr_album.addWidget(self.caja_canciones)

        self.widget_botones = QWidget()
        self.widget_botones.setLayout(QHBoxLayout())
        self.distr_album.addWidget(self.widget_botones)

        self.widget_botones.layout().addWidget(self.boton_buscar)
        self.widget_botones.layout().addWidget(self.boton_nuevo)
        self.widget_botones.layout().addWidget(self.boton_interpretes)
        self.widget_botones.layout().addWidget(self.boton_albumes)

    def crear_campo_texto(self, texto, edit=True):
        campo = QLineEdit(texto)
        if not edit:
            campo.setReadOnly(True)
        return campo

    def limpiar_canciones(self):
        while self.caja_canciones.layout().count()>len(self.titulos):
            child = self.caja_canciones.layout().takeAt(len(self.titulos))
            if child.widget():
                child.widget().deleteLater()

    def mostrar_canciones(self, canciones):
        self.limpiar_canciones()
        self.botones = []
        
        for i in range(len(canciones)):
            texto_titulo = QLineEdit(canciones[i]["titulo"])
            texto_titulo.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_titulo,i+1,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            texto_interpretes = QLineEdit(canciones[i].get("interpretes",""))
            texto_interpretes.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_interpretes,i+1,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            
            texto_duracion = QLineEdit("{}:{}".format(canciones[i]["minutos"],canciones[i]["segundos"]))
            texto_duracion.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_duracion,i+1,2, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            
            self.botones.append((QPushButton("Ver"),QPushButton("Borrar")))
            self.botones[i][0].setFixedWidth(50)
            self.botones[i][1].setFixedWidth(50)
            self.botones[i][0].clicked.connect(lambda estado, x=canciones[i]["id"]: self.ver_cancion(x))
            self.botones[i][1].clicked.connect(lambda estado, x=canciones[i]["id"]: self.borrar_cancion(x))

            widget_botones = QWidget()
            widget_botones.setLayout(QGridLayout())
            widget_botones.setFixedWidth(110)
        
            widget_botones.layout().addWidget(self.botones[i][0],0,0)
            widget_botones.layout().addWidget(self.botones[i][1],0,1)
            widget_botones.layout().setContentsMargins(0,0,0,0)

            self.caja_canciones.layout().addWidget(widget_botones, i+1,3)
            self.caja_canciones.layout().setAlignment(widget_botones , QtCore.Qt.AlignTop )

    
    def ver_cancion(self, id_cancion):
        self.interfaz.mostrar_ventana_cancion(id_cancion)
        self.hide()

    def borrar_cancion(self, id_cancion):
        self.interfaz.eliminar_cancion(id_cancion)


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

            self.dialogo_nueva_cancion.setWindowTitle("Añadir nuevo album")
            self.dialogo_nueva_cancion.exec_()
            self.dialogo_nueva_cancion.close()

    def crear_cancion(self, dict_cancion):
        self.dialogo_nueva_cancion.close()
        self.interfaz.crear_cancion(dict_cancion)
        

    def ver_interpretes(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_interpretes()   

    def ver_albumes(self):
        self.hide()
        self.interfaz.mostrar_ventana_lista_albums()   

    def buscar(self):
        self.hide()
        self.interfaz.mostrar_ventana_buscar()
