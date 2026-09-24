import pyttsx3
import os
import webbrowser

from Clases.Busqueda import Busqueda

class Helper:

    try:
        voz = pyttsx3.init()
        voz.setProperty("rate", 175)
        voz.setProperty("volume", 1.0)
    except Exception:
        voz = None

    @staticmethod
    def hablar(texto):

        if not texto:
            return

        print(f"Aurora: {texto}")

        if Helper.voz is not None:
            try:
                Helper.voz.say(texto)
                Helper.voz.runAndWait()

            except Exception as e:
                print("Error en voz:", e)

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
            return

        print(f"Abriendo {app}")

        if not Busqueda.busqueda_profunda(app):

            webbrowser.open(
                f"https://www.google.com/search?q={app}"
            )