import sys
from modelo.declarative_base import session, Base, engine
import vista.interfaz_coleccion as ic
from logica.Coleccion import Coleccion

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session.close()
    
    coleccion = Coleccion()

    app = ic.App(sys.argv, coleccion)
    sys.exit(app.exec_())
