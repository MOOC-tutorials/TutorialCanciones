import unittest

from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.declarative_base import Session


class AlbumTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()

    def testAgregarAlbum(self):
        self.coleccion.agregar_album("Mio", 2000, "Sin descripción", "CD")
        self.coleccion.agregar_album("Clara luna", 1992, "Sin descripción", "CASETE")
        self.consulta1 = self.session.query(Album).filter(Album.titulo == "Mio").first()
        self.consulta2 = self.session.query(Album).filter(Album.id == 2).first()
        self.assertEqual(self.consulta1.titulo, "Mio")
        self.assertIsNotNone(self.consulta2)

    def testEditarAlbum(self):
        self.coleccion.editar_album(2, "Clara luna-Mix", 1982, "Sin descripción", "DISCO")
        self.consulta = self.session.query(Album).filter(Album.id == 2).first()
        self.assertIsNot(self.consulta.titulo, "Clara luna")

    def testEliminarAlbum(self):
        self.coleccion.eliminar_album(1)
        self.consulta = self.session.query(Album).filter(Album.id == 1).first()
        self.assertIsNone(self.consulta)

    def testBuscarAlbumesPorTitulo(self):
        self.consulta1 = self.coleccion.buscar_albumes_por_titulo("clara luna")
        self.coleccion.agregar_album("Clara luna-Instrumental", 1992, "Sin descripción", "CD")
        self.consulta2 = self.coleccion.buscar_albumes_por_titulo("clara luna")
        self.assertGreater(len(self.consulta2), len(self.consulta1))

    def testDarAlbumPorId(self):
        self.coleccion.agregar_album("Infinito arcoiris", 1990, "Sin descripción", "CASETE")
        self.album_id = self.session.query(Album).filter(Album.titulo == "Infinito arcoiris").first().id
        self.consulta = self.coleccion.dar_album_por_id(self.album_id)["titulo"]
        self.assertEqual(self.consulta, "Infinito arcoiris")

    def testDarAlbumes(self):
        self.consulta1 = self.coleccion.dar_albumes()
        self.coleccion.agregar_album("New life", 2018, "Album escrito para...", "CD")
        self.consulta2 = self.coleccion.dar_albumes()
        self.assertGreater(len(self.consulta2), len(self.consulta1))
