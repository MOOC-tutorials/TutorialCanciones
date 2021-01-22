from src.modelo.album import Album, Medio
from src.modelo.cancion import Cancion
from src.modelo.declarative_base import session, engine, Base
from src.modelo.interprete import Interprete


class Coleccion():

    def __init__(self):
        Base.metadata.create_all(engine)

    def darAlbumes(self):
        albumes = [elem.__dict__ for elem in session.query(Album).all()]
        return albumes

    def darCancionesDeAlbum(self, album_id):
        canciones = [elem.__dict__ for elem in
                     session.query(Cancion).filter(Cancion.albumes.any(Album.id.in_([album_id]))).all()]
        return canciones

    def darCanciones(self):
        canciones = [elem.__dict__ for elem in session.query(Cancion).all()]
        return canciones

    def darInterpretes(self):
        interpretes = [elem.__dict__ for elem in session.query(Interprete).all()]
        return interpretes

    def darInterpretesDeAlbum(self, album_id):
        canciones = session.query(Cancion).filter(Cancion.albumes.any(Album.id.in_([album_id]))).all()
        interpretes = []
        for cancion in canciones:
            for interprete in cancion.interpretes:
                interpretes.append(interprete.nombre)
        return interpretes

    def darAlbumPorId(self, album_id):
        return session.query(Album).get(album_id).__dict__

    def darInterpretePorId(self, interprete_id):
        return session.query(Interprete).filter_by(id=interprete_id).first().__dict__

    def darCancionPorId(self, cancion_id):
        cancion = session.query(Cancion).filter_by(id=cancion_id).first()
        cancion_dict = cancion.__dict__
        cancion_dict["interpretes"] = [self.darInterpretePorId(interprete.id) for interprete in cancion.interpretes]
        return cancion_dict

    def buscarAlbumesPorTitulo(self, album_titulo):
        albumes = [elem.__dict__ for elem in
                   session.query(Album).filter(Album.titulo.ilike('%{0}%'.format(album_titulo))).all()]
        return albumes

    def buscarCancionesPorTitulo(self, cancion_titulo):
        canciones = [elem.__dict__ for elem in
                     session.query(Cancion).filter(Cancion.titulo.ilike('%{0}%'.format(cancion_titulo))).all()]
        return canciones

    def buscarInterpretesPorNombre(self, interprete_nombre):
        interpretes = [elem.__dict__ for elem in session.query(Interprete).filter(
            Interprete.nombre.ilike('%{0}%'.format(interprete_nombre))).all()]
        return interpretes

    def buscarCancionesPorInterprete(self, interprete_nombre):
        canciones = [elem.__dict__ for elem in session.query(Cancion).filter(
            Cancion.interpretes.any(Interprete.nombre.ilike('%{0}%'.format(interprete_nombre)))).all()]
        return canciones

    def agregarAlbum(self, titulo, anio, descripcion, medio):
        try:
            album = Album(titulo=titulo, ano=anio, descripcion=descripcion, medio=medio)
            session.add(album)
            session.commit()
            return True
        except:
            return False

    def agregarCancion(self, titulo, minutos, segundos, compositor, album_id, interpretes_id):
        interpretesCancion = []
        if album_id > 0:
            busqueda = session.query(Cancion).filter(Cancion.albumes.any(Album.id.in_([album_id])),
                                                     Cancion.titulo == titulo).all()
            if len(busqueda) == 0:
                album = session.query(Album).filter(Album.id == album_id).first()
                for item in interpretes_id:
                    interprete = session.query(Interprete).filter(Interprete.id == item).first()
                    interpretesCancion.append(interprete)
                nuevaCancion = Cancion(titulo=titulo, minutos=minutos, segundos=segundos, compositor=compositor,
                                       albumes=[album], interpretes=interpretesCancion)
                session.add(nuevaCancion)
                session.commit()
                return True
            else:
                return False
        else:
            for item in interpretes_id:
                interprete = session.query(Interprete).filter(Interprete.id == item).first()
                interpretesCancion.append(interprete)
            nuevaCancion = Cancion(titulo=titulo, minutos=minutos, segundos=segundos, compositor=compositor,
                                   interpretes=interpretesCancion)
            session.add(nuevaCancion)
            session.commit()
            return True

    def agregarInterprete(self, nombre, texto_curiosidades, cancion_id):
        busqueda = session.query(Interprete).filter(Interprete.nombre == nombre).all()
        if len(busqueda) == 0:
            nuevoInterprete = Interprete(nombre=nombre, texto_curiosidades=texto_curiosidades, cancion=cancion_id)
            session.add(nuevoInterprete)
            session.commit()
            return True
        else:
            return False

    def eliminarAlbum(self, album_id):
        try:
            album = session.query(Album).filter(Album.id == album_id).first()
            session.delete(album)
            session.commit()
            return True
        except:
            return False

    def eliminarCancion(self, cancion_id):
        try:
            cancion = session.query(Cancion).filter(Cancion.id == cancion_id).first()
            session.delete(cancion)
            session.commit()
            return True
        except:
            return False

    def eliminarInterprete(self, interprete_id):
        try:
            interprete = session.query(Interprete).filter(Interprete.id == interprete_id).first()
            session.delete(interprete)
            session.commit()
            return True
        except:
            return False

    def editarAlbum(self, album_id, titulo, anio, descripcion, medio):
        try:
            album = session.query(Album).filter(Album.id == album_id).first()
            if titulo:
                album.titulo = titulo
            if anio:
                album.ano = anio
            if descripcion:
                album.descripcion = descripcion
            if medio:
                album.medio = medio
            session.commit()
            return True
        except:
            return False

    def editarCancion(self, cancion_id, titulo, minutos, segundos, compositor, interpretes_id):
        try:
            cancion = session.query(Cancion).filter(Cancion.id == cancion_id).first()
            cancion.titulo = titulo
            cancion.minutos = minutos
            cancion.segundos = segundos
            cancion.compositor = compositor
            interpretesCancion = []
            for item in interpretes_id:
                interprete = session.query(Interprete).filter(Interprete.id == item).first()
                interpretesCancion.append(interprete)
            cancion.interpretes = interpretesCancion
            session.commit()
            return True
        except:
            return False

    def editarInterprete(self, interprete_id, nombre, texto_curiosidades):
        busqueda = session.query(Interprete).filter(Interprete.id != interprete_id, Interprete.nombre == nombre).all()
        if len(busqueda) == 0:
            interprete = session.query(Interprete).filter(Interprete.id == interprete_id).first()
            interprete.nombre = nombre
            interprete.texto_curiosidades = texto_curiosidades
            session.commit()
            return True
        else:
            return False

    def darMedios(self):
        return [medio.name for medio in Medio]

    def asociarCancion(self, cancion_id, album_id):
        cancion = session.query(Cancion).filter(Cancion.id == cancion_id).first()
        album = session.query(Album).filter(Album.id == album_id).first()
        if cancion is not None and album is not None:
            album.canciones.append(cancion)
            session.commit()
            return True
        else:
            return False

    def asociarInterprete(self, cancion_id, interprete_id):
        cancion = session.query(Cancion).filter(Cancion.id == cancion_id).first()
        interprete = session.query(Interprete).filter(Interprete.id == interprete_id).first()
        if cancion is not None and interprete is not None:
            cancion.interpretes.append(interprete)
            session.commit()
            return True
        else:
            return False
