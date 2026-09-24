# Importación de paquetes

import speech_recognition as sr

class Escuchar:

    @staticmethod
    def escuchar(r):
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)

        try:
            return r.recognize_google(
                audio,
                language="es-AR"
            ).lower()

        except sr.UnknownValueError:
            return ""

        except sr.RequestError as e:
            print("Error con Google Speech:", e)
            return ""