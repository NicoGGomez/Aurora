import os
import shutil
import subprocess

class Busqueda:

    @staticmethod
    def abrir_vscode():

        # 1. Si "code" está agregado al PATH
        code = shutil.which("code")

        if code:
            subprocess.Popen(
                [code],
                shell=False
            )
            return True

        # 2. Instalación normal por usuario
        ruta_usuario = os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
        )

        if os.path.exists(ruta_usuario):
            subprocess.Popen(
                [ruta_usuario]
            )
            return True

        # 3. Instalación para todos los usuarios
        ruta_programas = os.path.expandvars(
            r"%ProgramFiles%\Microsoft VS Code\Code.exe"
        )

        if os.path.exists(ruta_programas):
            subprocess.Popen(
                [ruta_programas]
            )
            return True

        # 4. Instalación 32 bits
        ruta_programas_x86 = os.path.expandvars(
            r"%ProgramFiles(x86)%\Microsoft VS Code\Code.exe"
        )

        if os.path.exists(ruta_programas_x86):
            subprocess.Popen(
                [ruta_programas_x86]
            )
            return True

        print("❌ No encontré Visual Studio Code")
        return False

    @staticmethod
    def busqueda_profunda(aplicacion):

        posibles_rutas = [

            # Usuario
            os.path.expandvars(
                rf"%APPDATA%\{aplicacion}\{aplicacion}.exe"
            ),

            os.path.expandvars(
                rf"%LOCALAPPDATA%\{aplicacion}\{aplicacion}.exe"
            ),

            # Microsoft Store
            os.path.expandvars(
                rf"%LOCALAPPDATA%\Microsoft\WindowsApps\{aplicacion}.exe"
            ),

            # Program Files
            rf"C:\Program Files\{aplicacion}\{aplicacion}.exe",
            rf"C:\Program Files (x86)\{aplicacion}\{aplicacion}.exe",

            # Variantes
            rf"C:\Program Files\{aplicacion.capitalize()}\{aplicacion}.exe",
            rf"C:\Program Files (x86)\{aplicacion.capitalize()}\{aplicacion}.exe",

            # Ejecutable directo
            rf"C:\Program Files\{aplicacion}.exe",
            rf"C:\Program Files (x86)\{aplicacion}.exe",

            # LocalAppData
            os.path.expandvars(
                rf"%LOCALAPPDATA%\Programs\{aplicacion}\{aplicacion}.exe"
            ),

            os.path.expandvars(
                rf"%LOCALAPPDATA%\Programs\{aplicacion.capitalize()}\{aplicacion}.exe"
            ),

            # Escritorio
            os.path.expandvars(
                rf"%USERPROFILE%\Desktop\{aplicacion}.exe"
            ),

            # Descargas
            os.path.expandvars(
                rf"%USERPROFILE%\Downloads\{aplicacion}.exe"
            ),
        ]

        for ruta in posibles_rutas:

            if os.path.exists(ruta):

                print(f"Encontrado: {ruta}")

                os.startfile(ruta)

                return True

        print(f"No se encontró {aplicacion}")

        return False