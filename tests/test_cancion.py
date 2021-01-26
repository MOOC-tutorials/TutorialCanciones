import unittest

from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.cancion import Cancion
from src.modelo.declarative_base import Session
from src.modelo.interprete import Interprete


class CancionTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()

    def testAgregarCancionSinAlbum(self):
        self.coleccion.agregar_interprete("Vicente Fernandez", "Grabado en 3 potrillos", -1)
        self.coleccion.agregar_interprete("Alejandro Fernandez", "En honor al aniversario...", -1)
        self.coleccion.agregar_cancion("Felicidad", 3, 10, "Desconocido", -1,
                                       [{'nombre': 'Vicente Fernandez', 'texto_curiosidades': 'Grabado en 3 potrillos'},
                                        {'nombre': 'Alejandro Fernandez',
                                         'texto_curiosidades': 'En honor al aniversario...'}])
        self.consulta1 = self.session.query(Cancion).filter(Cancion.titulo == "Felicidad").first()
        self.assertIsNotNone(self.consulta1)

    def testAgregarCancionConAlbum(self):
        self.coleccion.agregar_album("Renacer", 2005, "Sin descripción", "CD")
        self.consulta1 = self.session.query(Album).filter(Album.titulo == "Renacer").first().id
        self.coleccion.agregar_interprete("Alejandra Guzman", "Canción dedicada a su ...", -1)
        self.coleccion.agregar_cancion("Bye mamá", 1, 48, "Desconocido", self.consulta1,
                                       [{'nombre': 'Alejandra Guzman',
                                         'texto_curiosidades': 'Canción dedicada a su ...'}])
        self.consulta2 = self.session.query(Cancion).filter(Cancion.titulo == "Bye mamá").first()
        self.assertIsNotNone(self.consulta2)

    def testEditarCancionSinCambiarInterpretes(self):
        self.coleccion.editar_cancion(1, "Bye mamá", 2, 54, "J.R.Florez",
                                      [{'id': '2', 'nombre': 'Alejandra Guzman',
                                        'texto_curiosidades': 'Canción dedicada a su ...'}])
        self.consulta = self.session.query(Cancion).filter(Cancion.id == 1).first()
        self.assertEqual(self.consulta.compositor, "J.R.Florez")

    def testEditarCancionInterpretes(self):
        self.consulta1 = self.session.query(Cancion).filter(Cancion.id == 1).first().compositor
        self.consulta2 = self.session.query(Interprete).filter(Interprete.nombre == "Franco de Vita").first()
        if self.consulta2 is None:
            self.coleccion.agregar_interprete("Franco de Vita", "Duo con más likes en redes", 1)
            self.coleccion.editar_cancion(1, "Bye mamá", 4, 23, "J.R.Florez y Difelisatti",
                                          [{'id': '2', 'nombre': 'Alejandra Guzman',
                                            'texto_curiosidades': 'Canción dedicada a su ...'},
                                           {'id': 'n', 'nombre': 'Franco de Vita',
                                            'texto_curiosidades': 'Duo con más likes en redes'}])
        else:
            self.coleccion.editar_cancion(1, "Bye bye", 4, 23, "J.R.Florez y Difelisatti",
                                          [{'id': '2', 'nombre': 'Alejandra Guzman',
                                            'texto_curiosidades': 'Canción dedicada a su ...'},
                                           {'id': '9', 'nombre': 'Franco de Vita',
                                            'texto_curiosidades': 'Duo con más likes en redes'}])
        self.consulta3 = self.session.query(Cancion).filter(Cancion.id == 1).first()
        self.assertEqual(self.consulta3.compositor, "J.R.Florez y Difelisatti")

    def testEliminarCancion(self):
        self.coleccion.eliminar_cancion(2)
        self.consulta = self.session.query(Cancion).filter(Cancion.id == 2).first()
        self.assertIsNone(self.consulta)

    def testBuscarCancionesPorTitulo(self):
        self.coleccion.agregar_album("Amapola azul", 2020, "Instrumental", "CD")
        self.consulta1 = self.session.query(Album).filter(Album.titulo == "Amapola azul").first().id
        self.coleccion.agregar_interprete("Andrea Echeverri", "En ese año nacio su hijo...", -1)
        self.coleccion.agregar_cancion("Baby blues", 3, 20, "Andrea Echeverri", self.consulta1,
                                       [{'nombre': 'Andrea Echeverri',
                                         'texto_curiosidades': 'En ese año nacio su hijo...'}])
        self.consulta = self.coleccion.buscar_canciones_por_titulo("Baby")
        self.assertGreater(len(self.consulta), 0)

    def testDarCancionPorId(self):
        self.consulta = self.coleccion.dar_cancion_por_id(1)
        self.assertEqual(self.consulta["titulo"], "Bye mamá")

    def testDarCanciones(self):
        self.consulta = self.coleccion.dar_canciones()
        self.assertNotEqual(self.consulta, [])
