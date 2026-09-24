import os

class Busqueda:

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