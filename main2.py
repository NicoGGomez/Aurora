import speech_recognition as sr
import os
import time
import urllib.parse
import pyautogui
import ctypes
from datetime import datetime
import pywhatkit
import re
import webbrowser
import winsound

import threading
import queue

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL, CoInitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

r = sr.Recognizer()
r.pause_threshold = 0.8
mic = sr.Microphone()
eventos = queue.Queue()
activo = False

def escuchar():
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)

    try:
        return r.recognize_google(audio, language="es-AR").lower()
    except sr.UnknownValueError:
        return ""

def listener():
    global activo

    while True:
        texto = escuchar()

        if texto:
            print("escuchado:", texto)

            # 🔥 WAKE WORD
            if "aurora" in texto:
                activo = True
                winsound.MessageBeep(winsound.MB_OK)
                print("🟢 Aurora activado")

            # si está activo, mandar a cola
            if activo:
                eventos.put(texto)
                activo = False  # se desactiva después de un comando

def processor():
    while True:
        texto = eventos.get()  # espera hasta que haya algo

        try:
            procesar_comando(texto)
        except Exception as e:
            print("error procesando comando:", e)


# VOLUMEN
def procesar_comando_volumen(texto):
    texto = texto.lower()

    if "mutear volumen" in texto:
        print("Volumen en 0%")
        set_volumen(0)

    elif "volumen máximo" in texto:
        print("Volumen en 100%")
        set_volumen(100)

    elif "volumen" in texto or "volumen al" in texto:
        porcentaje = obtener_porcentaje(texto)

        if porcentaje is not None:
            print(f"Acomodando volumen a {porcentaje}%")
            set_volumen(porcentaje)
        else:
            print("No se detectó porcentaje")

def obtener_porcentaje(texto):
    match = re.search(r"(?:volumen\s*)?(\d{1,3})\s*%?", texto)
    if match:
        print(match)
        return int(match.group(1))
    return None

def set_volumen(porcentaje):
    CoInitialize()
    enumerator = AudioUtilities.GetDeviceEnumerator()
    endpoint = enumerator.GetDefaultAudioEndpoint(0, 1)

    volume = endpoint.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(volume, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(porcentaje / 100, None)

# YOUTUBE

def procesar_comando_youtube(texto):
    texto = texto.lower()

    if "youtube" in texto:

        if "abrir" in texto:
            abrir_youtube()

        elif "buscar" in texto:
            manejar_busqueda_youtube(texto)

        elif "reproducir" in texto or "poner" in texto:
            manejar_play_youtube(texto)

        else:
            abrir_youtube()

def manejar_play_youtube(texto):
    query = limpiar_youtube(texto)

    if query:
        print("reproduciendo:", query)
        pywhatkit.playonyt(query)
    else:
        print("no entendí qué reproducir")

def manejar_busqueda_youtube(texto):
    query = limpiar_youtube(texto)

    if query:
        print("buscando en youtube:", query)

        import webbrowser
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
    else:
        print("no entendí qué buscar")

def limpiar_youtube(texto):
    palabras = ["aurora", "youtube", "en", "buscar en youtube", "buscar", "en youtube"]

    for p in palabras:
        texto = texto.replace(p, "")

    return texto.strip()

def abrir_youtube():
    print("abriendo youtube")
    webbrowser.open("https://www.youtube.com")

# COMANDOS

COMANDOS = {
    "youtube": procesar_comando_youtube,
    "volumen": procesar_comando_volumen
}

# ROUTER

def procesar_comando(texto):
    texto = texto.lower()
    print(texto)

    for clave, func in COMANDOS.items():
        if clave in texto:
            func(texto)
            return

    print("no entendí el comando")

if __name__ == "__main__":
    t1 = threading.Thread(target=listener, daemon=True)
    t2 = threading.Thread(target=processor, daemon=True)

    t1.start()
    t2.start()

    while True:
        time.sleep(1)