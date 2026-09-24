from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot

import speech_recognition as sr
import threading
import queue
import sys

from Clases.Sonido import Sonido
from Clases.Escuchar import Escuchar
from Clases.Notas import Notas
from Clases.Helper import Helper
from Clases.Comandos import Comandos
from Clases.ComandosCustom import ComandosCustom

from Datos.Respuestas import (
    SALUDOS,
    RESPUESTAS_ACTIVACION,
    RESPUESTAS_NO_ENTENDI
)


class AuroraBridge(QObject):

    estadoCambiado = Signal(str)
    comandoCambiado = Signal(str)

    @Slot(str)
    def cambiarEstado(self, estado):
        print(f"🖥️ Estado interfaz: {estado}")
        self.estadoCambiado.emit(estado)

    @Slot(str)
    def mostrarComando(self, comando):
        self.comandoCambiado.emit(comando)

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

    "buscar imagen" : Comandos.procesar_comando_buscar_imagen,

    "buscar" : Comandos.procesar_comando_buscar,

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

def procesar_comando(texto, bridge):

    texto = Helper.normalizar_texto(texto)

    print("🧠 Procesando:", texto)

    bridge.cambiarEstado("procesando")
    bridge.mostrarComando(texto)

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

            bridge.cambiarEstado("esperando")

            return

    print("❌ No entendí el comando")
    Helper.hablar(
        Helper.respuesta_aleatoria(
                RESPUESTAS_NO_ENTENDI
        )
    )
    bridge.cambiarEstado("esperando")


# =========================
# LISTENER
# =========================

def listener(bridge):

    with microfono as source:

        while ejecutando.is_set():

            bridge.cambiarEstado("escuchando")

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

                bridge.cambiarEstado("hablando")

                Helper.hablar(
                    Helper.respuesta_aleatoria(
                        RESPUESTAS_ACTIVACION
                    )
                )

                bridge.cambiarEstado("escuchando")

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

                    bridge.mostrarComando(comando)

                    eventos.put(comando)


# =========================
# PROCESSOR THREAD
# =========================

def processor(bridge):

    while ejecutando.is_set():

        try:

            texto = eventos.get(
                timeout=0.5
            )

            procesar_comando(texto, bridge)

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

# if __name__ == "__main__":

#     Helper.hablar(
#         Helper.respuesta_aleatoria(
#             SALUDOS
#         )
#     )

#     t1 = threading.Thread(
#         target=listener,
#         daemon=True
#     )

#     t2 = threading.Thread(
#         target=processor,
#         daemon=True
#     )

#     t1.start()
#     t2.start()

#     # Mantener el programa mientras Aurora esté activa
#     while ejecutando.is_set():

#         time.sleep(0.5)

#     print("🔴 Aurora desconectada")

if __name__ == "__main__":

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    bridge = AuroraBridge()

    engine.rootContext().setContextProperty(
        "aurora",
        bridge
    )

    engine.load(
        "Interfaz/Main.qml"
    )

    if not engine.rootObjects():
        sys.exit(-1)

    bridge.cambiarEstado("escuchando")

    Helper.hablar(
        Helper.respuesta_aleatoria(
            SALUDOS
        )
    )

    t1 = threading.Thread(
        target=listener,
        args=(bridge,),
        daemon=True
    )

    t2 = threading.Thread(
        target=processor,
        args=(bridge,),
        daemon=True
    )

    t1.start()
    t2.start()

    sys.exit(app.exec())