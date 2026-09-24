import pywhatkit
import webbrowser


class ComandoYT:

    @staticmethod
    def manejar_play_youtube(texto):

        query = ComandoYT.limpiar_youtube(texto)

        if query:

            print("Reproduciendo:", query)

            pywhatkit.playonyt(query)

        else:

            print("No entendí qué reproducir")

    @staticmethod
    def manejar_busqueda_youtube(texto):

        query = ComandoYT.limpiar_youtube(texto)

        if query:

            print("Buscando en YouTube:", query)

            url = (
                "https://www.youtube.com/results?search_query="
                + query.replace(" ", "+")
            )

            webbrowser.open(url)

        else:

            print("No entendí qué buscar")

    @staticmethod
    def limpiar_youtube(texto):

        palabras = [
            "aurora",
            "youtube",
            "en",
            "buscar en youtube",
            "buscar",
            "en youtube",
            "reproducir",
            "poner"
        ]

        for palabra in palabras:
            texto = texto.replace(palabra, "")

        return texto.strip()

    @staticmethod
    def abrir_youtube():

        print("Abriendo YouTube")

        webbrowser.open(
            "https://www.youtube.com"
        )