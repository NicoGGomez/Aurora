import speech_recognition as sr
import threading
import queue
import time

from Clases.Sonido import Sonido
from Clases.Escuchar import Escuchar
from Clases.Notas import Notas
from Clases.Helper import Helper
from Clases.Comandos import Comandos
from Clases.ComandosCustom import ComandosCustom

from Datos.Respuestas import (
    SALUDOS,
    RESPUESTAS_ACTIVACION
)


# =========================
# CONFIGURACIÓN
# =========================

r = sr.Recognizer()

r.pause_threshold = 0.8
r.non_speaking_duration = 0.5
r.phrase_threshold = 0.3

r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.dynamic_energy_ratio = 1.5

microfono = sr.Microphone()

eventos = queue.Queue()

# Evento para controlar la ejecución de Aurora
ejecutando = threading.Event()
ejecutando.set()


# =========================
# CALIBRAR MICRÓFONO
# =========================

with microfono as source:

    print("🎙️ Calibrando micrófono...")

    r.adjust_for_ambient_noise(
        source,
        duration=2
    )

print("🟢 Micrófono listo")


# =========================
# COMANDOS
# =========================

COMANDOS = {

    "desconectate": Comandos.desconectar,

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

    "reproducir": Sonido.procesar_sonido,

    "pausar": Sonido.procesar_sonido,

    "siguiente": Sonido.procesar_sonido,

    "anterior": Sonido.procesar_sonido,

    "pc": Comandos.procesar_comando_pc
}


# =========================
# PROCESADOR
# =========================

def procesar_comando(texto):

    texto = Helper.normalizar_texto(texto)

    print("🧠 Procesando:", texto)

    for clave, funcion in COMANDOS.items():

        if clave in texto:

            # Desconectar necesita recibir
            # el Event para poder detener Aurora
            if clave == "desconectate":

                funcion(
                    texto,
                    ejecutando
                )

            else:

                funcion(texto)

            return

    print("❌ No entendí el comando")


# =========================
# LISTENER
# =========================

def listener():

    with microfono as source:

        while ejecutando.is_set():

            texto = Escuchar.escuchar(
                r,
                source
            )

            # Verificamos si Aurora fue apagada
            if not ejecutando.is_set():
                break

            if not texto:
                continue

            # Normalizamos acentos
            texto = Helper.normalizar_texto(texto)

            print("👂 Escuchado:", texto)

            if "aurora" in texto:

                print("🟢 Aurora activada")

                Helper.hablar(
                    Helper.respuesta_aleatoria(
                        RESPUESTAS_ACTIVACION
                    )
                )

                comando = Escuchar.escuchar(
                    r,
                    source
                )

                # Si se desconectó mientras escuchaba
                if not ejecutando.is_set():
                    break

                if comando:

                    print(
                        "📥 Comando recibido:",
                        comando
                    )

                    eventos.put(comando)


# =========================
# PROCESSOR THREAD
# =========================

def processor():

    while ejecutando.is_set():

        try:

            texto = eventos.get(
                timeout=0.5
            )

            procesar_comando(texto)

        except queue.Empty:

            continue

        except Exception as e:

            print(
                "❌ Error procesando comando:",
                e
            )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    Helper.hablar(
        Helper.respuesta_aleatoria(
            SALUDOS
        )
    )

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

    # Mantener el programa mientras Aurora esté activa
    while ejecutando.is_set():

        time.sleep(0.5)

    print("🔴 Aurora desconectada")