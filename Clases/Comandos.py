import os
import pyautogui
import ctypes
import webbrowser

from Clases.ComandoYT import ComandoYT
from Clases.ComandoSpotify import ComandoSpotify
from Clases.Helper import Helper

from Datos.Respuestas import DESPEDIDAS


class Comandos:

    def procesar_comando_buscar(texto):
        texto = texto.lower().strip()

        palabras_busqueda = [
            "buscar",
            "buscá",
            "googlear",
            "googleá",
            "buscame",
            "buscá en google",
            "buscar en google"
        ]

        for palabra in palabras_busqueda:
            if palabra in texto:
                busqueda = texto.split(palabra, 1)[1].strip()

                if busqueda:
                    url = f"https://www.google.com/search?q={busqueda.replace(' ', '+')}"
                    webbrowser.open(url)

                    print(f"🔎 Buscando en Google: {busqueda}")
                    return True

        return False

    @staticmethod
    def procesar_comando_buscar_imagen(texto):
        texto = texto.lower().strip()

        palabras_busqueda = [
            "buscar imagen",
            "buscar imágenes",
            "buscá imagen",
            "buscá imágenes",
            "buscar foto",
            "buscar fotos",
            "buscá foto",
            "buscá fotos"
        ]

        for palabra in palabras_busqueda:
            if palabra in texto:
                busqueda = texto.split(palabra, 1)[1].strip()

                if busqueda:
                    url = (
                        "https://www.google.com/search"
                        f"?tbm=isch&q={busqueda.replace(' ', '+')}"
                    )

                    webbrowser.open(url)

                    print(f"🖼️ Buscando imagen: {busqueda}")
                    return True

        return False

    @staticmethod
    def procesar_comando_pc(texto):

        texto = texto.lower()

        if "bloquear" in texto:

            ctypes.windll.user32.LockWorkStation()

            Helper.hablar(
                Helper.respuesta_aleatoria(
                    DESPEDIDAS
                )
            )

        elif "suspender" in texto:

            os.system(
                "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
            )

        elif "reiniciar" in texto:

            os.system(
                "shutdown -r -t 0"
            )

        elif "apagar" in texto:

            os.system(
                "shutdown -s -t 0"
            )

        elif "abrir configuracion" in texto:

            os.system(
                "start ms-settings:"
            )

        elif "bluetooth" in texto:

            os.system(
                "start ms-settings:bluetooth"
            )

        elif "mostrar escritorio" in texto:

            pyautogui.hotkey(
                "win",
                "d"
            )

        elif "cerrar ventana" in texto:

            pyautogui.hotkey(
                "alt",
                "f4"
            )


    @staticmethod
    def mostrar_escritorio(texto):

        if "despejar" in texto:

            pyautogui.hotkey(
                "win",
                "d"
            )

            Helper.hablar(
                "Ya despejé la pantalla"
            )

        elif "cerrar" in texto:

            pyautogui.hotkey(
                "alt",
                "f4"
            )


    @staticmethod
    def procesar_comando_youtube(texto):

        texto = texto.lower()

        if "abrir" in texto:

            Helper.abrir_aplicacion(
                "youtube"
            )

        elif "buscar" in texto:

            ComandoYT.manejar_busqueda_youtube(
                texto
            )

        elif "reproducir" in texto or "poner" in texto:

            ComandoYT.manejar_play_youtube(
                texto
            )

        else:

            Helper.abrir_aplicacion(
                "youtube"
            )


    @staticmethod
    def procesar_comando_spotify(texto):

        print("llegue a spotify")

        texto = texto.lower().strip()

        if "abrir" in texto:

            ComandoSpotify.abrir_spotify()

        elif "reproducir" in texto or "reproduce" in texto:

            ComandoSpotify.reproducir_cancion_spotify(
                texto
            )


    @staticmethod
    def procesar_comando_vscode(texto):

        texto = texto.lower()

        if "abrir" in texto:

            Helper.abrir_aplicacion(
                "vscode"
            )


    @staticmethod
    def procesar_comando_whatsapp(texto):

        texto = texto.lower()

        if "abrir" in texto:

            Helper.abrir_aplicacion(
                "whatsapp"
            )


    @staticmethod
    def desconectar(
        texto=None,
        ejecutando=None
    ):

        # Primero habla
        Helper.hablar(
            Helper.respuesta_aleatoria(
                DESPEDIDAS
            )
        )

        # Reproducir sonido de desconexión COMPLETO
        Helper.sonido_activacion()

        # Recién ahora apagar Aurora
        if ejecutando is not None:
            ejecutando.clear()