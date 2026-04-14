import speech_recognition as sr
import os
import time
import urllib.parse
import pyautogui
import ctypes
from datetime import datetime
import pywhatkit
import re

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

r = sr.Recognizer()
r.pause_threshold = 0.8

mic = sr.Microphone()

def escuchar():
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)

    try:
        return r.recognize_google(audio, language="es-AR").lower()
    except sr.UnknownValueError:
        return ""
    
def limpiar_busqueda(texto):
    palabras_clave = ["reproducir", "poné", "poner", "buscá", "buscar", "youtube", "en", "internet", "aurora"]
    
    for palabra in palabras_clave:
        texto = texto.replace(palabra, "")
    
    return texto.strip()

def busqueda_profunda(aplicacion):
    posibles_rutas = [
        # Usuario
        os.path.expandvars(rf"%APPDATA%\{aplicacion}\{aplicacion}.exe"),
        os.path.expandvars(rf"%LOCALAPPDATA%\{aplicacion}\{aplicacion}.exe"),

        # Microsoft Store
        os.path.expandvars(rf"%LOCALAPPDATA%\Microsoft\WindowsApps\{aplicacion}.exe"),

        # Program Files
        rf"C:\Program Files\{aplicacion}\{aplicacion}.exe",
        rf"C:\Program Files (x86)\{aplicacion}\{aplicacion}.exe",

        # Variantes comunes
        rf"C:\Program Files\{aplicacion.capitalize()}\{aplicacion}.exe",
        rf"C:\Program Files (x86)\{aplicacion.capitalize()}\{aplicacion}.exe",
    ]

    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            os.startfile(ruta)
            return True

    print(f"No se encontró {aplicacion}")
    return False

def tomar_nota(nota):
    if nota:
        with open("notas.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%d/%m %H:%M')}] {nota}\n")

        print("nota guardada")

        os.system("start notas.txt")
    else:
        print("no entendí la nota")

def obtener_porcentaje(texto):
    match = re.search(r"(?:volumen\s*)?(\d{1,3})\s*%?", texto)
    if match:
        return int(match.group(1))
    return None

def play_pause():
    pyautogui.press("playpause")

def next_song():
    pyautogui.press("nexttrack")

def prev_song():
    pyautogui.press("prevtrack")

def set_volumen(porcentaje):
    enumerator = AudioUtilities.GetDeviceEnumerator()
    endpoint = enumerator.GetDefaultAudioEndpoint(0, 1)

    volume = endpoint.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(volume, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(porcentaje / 100, None)

def bajar_volumen():
    pyautogui.press("volumedown")

def subir_volumen():
    pyautogui.press("volumeup")

def suspender_pc():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def bloquear_pc():
    ctypes.windll.user32.LockWorkStation()


# FUNCIONES 

def manejar_youtube(texto):
    print("procesando youtube...")

    # limpiar comando
    busqueda = texto.replace("aurora", "")
    busqueda = busqueda.replace("buscar en youtube", "")
    busqueda = busqueda.replace("youtube", "")
    busqueda = busqueda.strip()

    if busqueda:
        print("reproduciendo:", busqueda)
        pywhatkit.playonyt(busqueda)
    else:
        print("no entendí qué buscar en youtube")


# BUCLE

while True:
    texto = escuchar()

    if not texto:
        continue

    print("escuchado:", texto)

    # ------------------------
    # GENERALES
    # ------------------------

    if "aurora volumen máximo" in texto or "aurora volumen maximo" in texto :
        set_volumen(100)

    elif "aurora mutear volumen" in texto:
        set_volumen(0)

    elif "aurora volumen" in texto:
        porcentaje = obtener_porcentaje(texto)

        if porcentaje is not None:
            print(f"Acomodando volumen a {porcentaje}%")
            set_volumen(porcentaje)

    elif "aurora volver a reproducir" in texto:
        print("toggle play/pause")
        prev_song()

    elif "aurora reproducir anterior" in texto:
        print("toggle play/pause")
        prev_song()
        prev_song()

    elif "aurora reproducir siguiente" in texto:
        print("toggle play/pause")
        next_song()

    elif "aurora reproducir sonido" in texto or "aurora pausar sonido" in texto:
        print("toggle play/pause")
        play_pause()

    elif "aurora computadora en modo reposo" in texto:
        print("poniendo la pc en reposo")
        suspender_pc()

    elif "aurora bloquear pc" in texto or "aurora bloquear computadora" in texto:
        print("bloqueando pc")
        bloquear_pc()

    # ------------------------
    # NOTAS
    # ------------------------

    elif "aurora toma nota" in texto:
        print("modo dictado activado")

        nombre_archivo = f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        os.system(f"start notepad {nombre_archivo}")
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(">>> Decí 'aurora finalizar nota' para terminar <<<\n")
            f.write("\n")
        
        time.sleep(1.5)  # esperar que abra

        while True:
            nota = escuchar()
            pyautogui.hotkey('ctrl', 'end')
            pyautogui.press('enter')

            if not nota:
                continue

            if "aurora finalizar nota" in nota:
                print("nota finalizada")
                pyautogui.hotkey('ctrl', 'end')
                pyautogui.press('enter')
                pyautogui.press('enter')
                pyautogui.write(f"fin de la nota! fecha: {datetime.now().strftime('%d/%m/%Y')}")
                break

            # escribir en el bloc abierto
            pyautogui.write(nota + " ", interval=0.02)
            
    # ------------------------
    # CHATGPT
    # ------------------------

    elif "aurora abrir chat gpt" in texto:
        print("abriendo chat gpt")
        try:
            os.system("start chatgpt")
        except:
            os.system("start https://chat.openai.com")

    # ------------------------
    # YOUTUBE
    # ------------------------

    elif "aurora abrir youtube" in texto:
        print("abriendo youtube")
        os.system("start https://www.youtube.com")

    elif "aurora buscar en youtube" in texto:
        print("reproduciendo en youtube")

        busqueda = limpiar_busqueda(texto)

        if busqueda:
            pywhatkit.playonyt(busqueda)
        else:
            print("no entendí qué reproducir")

    # ------------------------
    # SPOTIFY
    # ------------------------

    elif "aurora abrir spotify" in texto:
        print("abriendo spotify")
        busqueda_profunda("Spotify")

    elif "aurora cerrar spotify" in texto:
        print("cerrando spotify")
        os.system("taskkill /f /im spotify.exe")

    # ------------------------
    # INTERNET
    # ------------------------

    elif "aurora buscar en internet" in texto:
        print("buscando en internet")

        busqueda = limpiar_busqueda(texto)

        if busqueda:
            query = urllib.parse.quote(busqueda)
            url = f"https://www.google.com/search?q={query}"
            os.system(f"start {url}")
        else:
            print("no entendí qué buscar")

    # ------------------------
    # COMANDO UNIVERSAL (🔥)
    # ------------------------

    elif "aurora abrir" in texto:
        app = texto.replace("aurora abrir", "").strip()

        if app:
            print(f"abriendo {app}")

            if os.system(f"start {app}") != 0:
                if not busqueda_profunda(app):
                    print("no se pudo abrir")

    time.sleep(0.5)
