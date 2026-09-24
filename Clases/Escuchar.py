import speech_recognition as sr


class Escuchar:

    @staticmethod
    def escuchar(r, source):

        try:

            audio = r.listen(
                source,
                timeout=1,
                phrase_time_limit=5
            )

            return r.recognize_google(
                audio,
                language="es-AR"
            ).lower()

        except sr.WaitTimeoutError:

            return None

        except sr.UnknownValueError:

            return None

        except sr.RequestError as e:

            print(
                "❌ Error con Google Speech:",
                e
            )

            return None

        except Exception as e:

            print(
                "❌ Error escuchando:",
                e
            )

            return None