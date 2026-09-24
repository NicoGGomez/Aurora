import re
import pyautogui

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL, CoInitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class Sonido:

    @staticmethod
    def set_volumen(porcentaje):

        CoInitialize()

        enumerator = AudioUtilities.GetDeviceEnumerator()

        endpoint = enumerator.GetDefaultAudioEndpoint(0, 1)

        volume = endpoint.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        volume = cast(
            volume,
            POINTER(IAudioEndpointVolume)
        )

        porcentaje = max(0, min(100, porcentaje))

        volume.SetMasterVolumeLevelScalar(
            porcentaje / 100,
            None
        )

    @staticmethod
    def obtener_porcentaje(texto):

        match = re.search(
            r"(?:volumen\s*)?(\d{1,3})\s*%?",
            texto
        )

        if match:
            return int(match.group(1))

        return None

    @staticmethod
    def procesar_comando_volumen(texto):

        texto = texto.lower()

        if "mutear volumen" in texto:

            Sonido.set_volumen(0)

        elif "volumen máximo" in texto:

            Sonido.set_volumen(100)

        elif "volumen" in texto:

            porcentaje = Sonido.obtener_porcentaje(texto)

            if porcentaje is not None:

                print(
                    f"Acomodando volumen a {porcentaje}%"
                )

                Sonido.set_volumen(porcentaje)

    @staticmethod
    def procesar_sonido(texto):

        texto = texto.lower()

        if "reproducir" in texto or "pausar" in texto:

            pyautogui.press("playpause")

        elif "siguiente" in texto:

            pyautogui.press("nexttrack")

        elif "anterior" in texto:

            pyautogui.press("prevtrack")