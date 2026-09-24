import speech_recognition as sr
import time
import threading
import queue

from Clases.Sonido import Sonido
from Clases.Escuchar import Escuchar
from Clases.Notas import Notas
from Clases.Helper import Helper
from Clases.Comandos import Comandos
from Clases.ComandosCustom import ComandosCustom


r = sr.Recognizer()
r.pause_threshold = 0.8

eventos = queue.Queue()

activo = False


def processor():

    while True:

        texto = eventos.get()

        try:

            procesar_comando(texto)

        except Exception as e:

            print(
                "Error procesando comando:",
                e
            )


def listener():

    global activo

    while True:

        texto = Escuchar.escuchar(r)

        if not texto:
            continue

        print("Escuchado:", texto)

        if "aurora" in texto:

            activo = True

            print("🟢 Aurora activado")

            eventos.put(texto)

            activo = False


COMANDOS = {

    "abrir": Helper.abrir_aplicacion,

    "visual": Comandos.procesar_comando_vscode,

    "programar": ComandosCustom.comando_programar,

    "pantalla": Comandos.mostrar_escritorio,

    "whatsapp": Comandos.procesar_comando_whatsapp,

    "youtube": Comandos.procesar_comando_youtube,

    "spotify": Comandos.procesar_comando_spotify,

    "volumen": Sonido.procesar_comando_volumen,

    "nota": Notas.procesar_comando_nota,

    "sonido": Sonido.procesar_sonido,

    "pc": Comandos.procesar_comando_pc
}


def procesar_comando(texto):

    texto = texto.lower()

    print(
        "Procesando:",
        texto
    )

    for clave, funcion in COMANDOS.items():

        if clave in texto:

            funcion(texto)

            return

    print(
        "No entendí el comando"
    )


if __name__ == "__main__":

    t1 = threading.Thread(
        target=listener,
        daemon=True
    )

    t2 = threading.Thread(
        target=processor,
        daemon=True
    )

    t1.start()
    t2.start()

    while True:

        time.sleep(1)