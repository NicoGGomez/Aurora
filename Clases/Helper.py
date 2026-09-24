import pyttsx3
import os
import webbrowser
import random
import winsound
import unicodedata

from Clases.Busqueda import Busqueda

class Helper:

    @staticmethod
    def hablar(texto):

        if not texto:
            return

        print(f"Aurora: {texto}")

        try:

            voz = pyttsx3.init()

            voz.setProperty("rate", 175)
            voz.setProperty("volume", 1.0)

            voz.say(texto)
            voz.runAndWait()

            voz.stop()

        except Exception as e:

            print("❌ Error en voz:", e)

    @staticmethod
    def limpiar_busqueda(texto):

        palabras_clave = [
            "aurora",
            "abrir",
            "reproducir",
            "poné",
            "poner",
            "buscá",
            "buscar",
            "youtube",
            "en",
            "internet"
        ]

        for palabra in palabras_clave:
            texto = texto.replace(palabra, "")

        return texto.strip()

    @staticmethod
    def abrir_aplicacion(app):

        app = app.lower()

        app = Helper.limpiar_busqueda(app)

        if "configuracion" in app:

            os.system("start ms-settings:")

        else:

            print(f"Abriendo {app}")

            if not Busqueda.busqueda_profunda(app):

                webbrowser.open(
                    f"https://www.google.com/search?q={app}"
                )

    @staticmethod
    def respuesta_aleatoria(respuestas):
        return random.choice(respuestas)

    @staticmethod
    def sonido_activacion():

        winsound.PlaySound(
            "Sonidos/activacion.wav",
            winsound.SND_FILENAME
        )

    def normalizar_texto(texto):

        texto = texto.lower().strip()

        texto = unicodedata.normalize(
            "NFD",
            texto
        )

        texto = "".join(
            c for c in texto
            if unicodedata.category(c) != "Mn"
        )

        return texto