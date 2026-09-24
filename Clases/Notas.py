import os
import time
import pyautogui
from datetime import datetime

from Clases.Escuchar import Escuchar


class Notas:

    @staticmethod
    def procesar_comando_nota(texto, r):

        texto = texto.lower()

        if "tomar nota" in texto:

            Notas.tomar_nota(r)

    @staticmethod
    def tomar_nota(r):

        nombre_archivo = (
            f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(
            nombre_archivo,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                ">>> Decí 'aurora finalizar nota' para terminar <<<\n\n"
            )

        os.system(
            f'start notepad "{nombre_archivo}"'
        )

        time.sleep(1.5)

        pyautogui.hotkey("ctrl", "end")
        pyautogui.press("enter")

        while True:

            nota = Escuchar.escuchar(r)

            if not nota:
                continue

            if "aurora finalizar nota" in nota:

                print("Nota finalizada")

                pyautogui.press("enter")

                pyautogui.write(
                    f"\n--- FIN DE LA NOTA "
                    f"({datetime.now().strftime('%d/%m/%Y')}) ---\n"
                )

                break

            pyautogui.write(
                nota + "\n",
                interval=0.02
            )