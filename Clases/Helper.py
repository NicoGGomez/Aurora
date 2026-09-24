import pyttsx3
import os
import webbrowser
import random
import winsound
import unicodedata
import subprocess
import webbrowser

from Clases.Busqueda import Busqueda
from Datos.Aplicaciones import APLICACIONES

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

        app = app.lower().strip()
        app = Helper.limpiar_busqueda(app)

        if "configuracion" in app:

            os.system("start ms-settings:")
            return

        # Si tenemos la aplicación en nuestro diccionario
        if app in APLICACIONES:

            for ejecutable in APLICACIONES[app]:

                try:

                    resultado = subprocess.run(
                        ["where", ejecutable],
                        capture_output=True,
                        text=True
                    )

                    if resultado.returncode == 0:

                        ruta = resultado.stdout.splitlines()[0]

                        print(f"✅ Encontrado: {ruta}")

                        subprocess.Popen(
                            ruta,
                            shell=True
                        )

                        return

                except Exception as e:

                    print(f"⚠️ Error: {e}")

        # Buscar aplicación de forma general
        print(f"🔎 Buscando {app}")

        if Busqueda.busqueda_profunda(app):
            return

        # Si no encontró nada → Google
        print(f"🌐 No encontré {app}")
        Helper.hablar(f"No encontré {app}, así que abrí la aplicación web")

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