
from PyQt5.QtWidgets import QComboBox, QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
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
        self.height = 200
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_cancion = QHBoxLayout()
        self.setLayout(self.distr_cancion)
        
        self.caja_datos = QGroupBox()
        layout_datos = QGridLayout()
        self.caja_datos.setLayout(layout_datos)

        datos = ["Canción", "Duración", "Intérpretes", "Compositor"]
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

        self.texto_interpretes = QLineEdit()
        self.texto_interpretes.setReadOnly(True)
        layout_datos.addWidget(self.texto_interpretes, 2, 1, 1, 3)

        self.texto_compositor = QLineEdit()
        layout_datos.addWidget(self.texto_compositor, 3, 1, 1, 3)

        self.caja_botones = QGroupBox()
        layout_botones = QVBoxLayout()
        self.caja_botones.setLayout(layout_botones)

        self.boton_guardar = QPushButton("Guardar datos editados")
        self.boton_guardar.clicked.connect(lambda: self.interfaz.guardar_cancion(self.cancion_actual["id"], {"titulo":self.texto_cancion.text(), "interpretes":self.texto_interpretes.text(), "minutos":self.texto_minutos.text(),"segundos":self.texto_segundos.text(),"compositor":self.texto_compositor.text(), "interpretes":[]}))
        layout_botones.addWidget(self.boton_guardar)

        self.boton_borrar = QPushButton("Borrar")
        self.boton_borrar.clicked.connect(lambda: self.interfaz.eliminar_cancion(self.cancion_actual["id"]))
        layout_botones.addWidget(self.boton_borrar)

        self.boton_adicionar = QPushButton("Adicionar Intérprete")
        self.boton_adicionar.clicked.connect(self.mostrar_dialogo_agregar_interprete)
        layout_botones.addWidget(self.boton_adicionar)

        self.boton_lista_canciones = QPushButton("Ver lista de canciones")
        self.boton_lista_canciones.clicked.connect(self.ver_canciones)
        layout_botones.addWidget(self.boton_lista_canciones)

        self.distr_cancion.addWidget(self.caja_datos)
        self.distr_cancion.addWidget(self.caja_botones)
        
    def mostrar_cancion(self, cancion):
        self.cancion_actual = cancion
        self.texto_cancion.setText(cancion["titulo"])
        self.texto_interpretes.setText(cancion.get("interpretes",";".join(cancion.get("interpretes",[]))))
        self.texto_minutos.setText(str(cancion["minutos"]))
        self.texto_segundos.setText(str(cancion["segundos"]))
        self.texto_compositor.setText(cancion["compositor"])

    def ver_canciones(self):
        self.interfaz.mostrar_ventana_lista_canciones()
        self.hide()

    def mostrar_dialogo_agregar_interprete(self):
        self.dialogo_agregar_interprete = QDialog(self)

        layout = QGridLayout()
        self.dialogo_agregar_interprete.setLayout(layout)
        self.dialogo_agregar_interprete.setFixedSize(400,100)

        lab1 = QLabel("Intérpretes")
        lista_interpretes = QComboBox()
        for interprete in self.interfaz.dar_interpretes():
            lista_interpretes.addItem(interprete["nombre"], interprete['id']) 
        layout.addWidget(lab1,0,0)
        layout.addWidget(lista_interpretes,0,1)
        
        widget_botones = QWidget()
        widget_botones.setFixedHeight(50)
        widget_botones.setLayout(QGridLayout())

        butAceptar = QPushButton("Agregar")
        butCancelar = QPushButton("Cancelar")

        widget_botones.layout().addWidget(butAceptar,0,0)
        widget_botones.layout().addWidget(butCancelar,0,1)

        layout.addWidget(widget_botones, 4,0,1,2)

        butAceptar.clicked.connect(lambda: self.asociar_interprete_a_cancion(lista_interpretes.itemData(lista_interpretes.currentIndex())))
        butCancelar.clicked.connect(lambda: self.dialogo_agregar_interprete.close())

        self.dialogo_agregar_interprete.setWindowTitle("Agregar intérprete")
        self.dialogo_agregar_interprete.exec_()

    def asociar_interprete_a_cancion(self, id_interprete):
        self.dialogo_agregar_interprete.close()
        self.interfaz.asociar_interprete_a_cancion(self.cancion_actual['id'], id_interprete)