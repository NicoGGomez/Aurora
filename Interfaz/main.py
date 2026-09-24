import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot


class AuroraBridge(QObject):

    estadoCambiado = Signal(str)
    comandoCambiado = Signal(str)

    @Slot(str)
    def cambiarEstado(self, estado):
        print(f"🔄 Estado: {estado}")
        self.estadoCambiado.emit(estado)

    @Slot(str)
    def mostrarComando(self, comando):
        print(f"📥 Comando: {comando}")
        self.comandoCambiado.emit(comando)


app = QApplication(sys.argv)

engine = QQmlApplicationEngine()

bridge = AuroraBridge()

# Exponemos Python a QML
engine.rootContext().setContextProperty("aurora", bridge)

# Cargamos la interfaz
engine.load("Interfaz/Main.qml")

if not engine.rootObjects():
    sys.exit(-1)

# 🧪 PRUEBA
bridge.cambiarEstado("escuchando")
bridge.mostrarComando("Hola Aurora")

sys.exit(app.exec())