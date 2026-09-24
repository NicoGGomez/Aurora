import os
import pyautogui
import ctypes

from Clases.ComandoYT import ComandoYT
from Clases.Helper import Helper


class Comandos:

    @staticmethod
    def procesar_comando_pc(texto):

        texto = texto.lower()

        if "bloquear" in texto:

            ctypes.windll.user32.LockWorkStation()

        elif "suspender" in texto:

            os.system(
                "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
            )

        elif "reiniciar" in texto:

            os.system("shutdown -r -t 0")

        elif "apagar" in texto:

            os.system("shutdown -s -t 0")

        elif "abrir configuracion" in texto:

            os.system("start ms-settings:")

        elif "bluetooth" in texto:

            os.system("start ms-settings:bluetooth")

        elif "mostrar escritorio" in texto:

            pyautogui.hotkey("win", "d")

        elif "cerrar ventana" in texto:

            pyautogui.hotkey("alt", "f4")

    @staticmethod
    def mostrar_escritorio(texto):

        if "despejar" in texto:

            pyautogui.hotkey("win", "d")

            Helper.hablar(
                "Ya despejé la pantalla"
            )

        elif "cerrar" in texto:

            pyautogui.hotkey("alt", "f4")

    @staticmethod
    def procesar_comando_youtube(texto):

        texto = texto.lower()

        if "abrir" in texto:

            Helper.abrir_aplicacion("youtube")

        elif "buscar" in texto:

            ComandoYT.manejar_busqueda_youtube(texto)

        elif "reproducir" in texto or "poner" in texto:

            ComandoYT.manejar_play_youtube(texto)

        else:

            Helper.abrir_aplicacion("youtube")

    @staticmethod
    def procesar_comando_spotify(texto):

        texto = texto.lower()

        if "abrir" in texto:

            Helper.abrir_aplicacion("spotify")

    @staticmethod
    def procesar_comando_vscode(texto):

        texto = texto.lower()

        if "abrir" in texto:

            Helper.abrir_aplicacion("vscode")

    @staticmethod
    def procesar_comando_whatsapp(texto):

        texto = texto.lower()

        if "abrir" in texto:

            Helper.abrir_aplicacion("whatsapp")