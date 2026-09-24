from Clases.Helper import Helper
from Clases.Busqueda import Busqueda
from Clases.ComandoSpotify import ComandoSpotify

class ComandosCustom:

    @staticmethod
    def comando_programar(texto=None):

        ComandoSpotify.reproducir_playlist_estudio()
        Helper.abrir_aplicacion("vscode")
        Helper.hablar("Ya esta todo listo para que empieces a programar")


        