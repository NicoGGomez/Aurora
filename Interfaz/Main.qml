import QtQuick
import QtQuick.Controls
import QtQuick.Window

Window {
    id: ventana

    width: 900
    height: 600

    visible: true
    title: "Aurora"

    color: "transparent"

    flags: Qt.FramelessWindowHint | Qt.Window

    Rectangle {
        id: fondo

        anchors.fill: parent

        color: "#0b0b12"
        radius: 25

        border.color: "#25253a"
        border.width: 1

        // ==========================================
        // COLOR PRINCIPAL DE AURORA
        // ==========================================

        property color colorAurora: "#7167ff"

        // ==========================================
        // TÍTULO
        // ==========================================

        Text {
            anchors.top: parent.top
            anchors.topMargin: 35
            anchors.horizontalCenter: parent.horizontalCenter

            text: "AURORA"

            color: "white"

            font.pixelSize: 28
            font.bold: true
        }

        // ==========================================
        // ESTADO
        // ==========================================

        Text {
            id: estadoTexto

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 90

            text: "Esperando..."

            color: fondo.colorAurora

            font.pixelSize: 16

            Behavior on color {
                ColorAnimation {
                    duration: 400
                }
            }
        }

        // ==========================================
        // NÚCLEO DE AURORA
        // ==========================================

        Rectangle {
            id: nucleo

            width: 180
            height: 180

            radius: width / 2

            anchors.centerIn: parent

            color: "#151522"

            border.width: 2
            border.color: fondo.colorAurora

            Behavior on border.color {
                ColorAnimation {
                    duration: 500
                }
            }

            // ======================================
            // AURA EXTERIOR
            // ======================================

            Rectangle {
                id: auraExterior

                width: 150
                height: 150

                radius: width / 2

                anchors.centerIn: parent

                color: fondo.colorAurora

                opacity: 0.08

                Behavior on color {
                    ColorAnimation {
                        duration: 500
                    }
                }
            }

            // ======================================
            // AURA INTERIOR
            // ======================================

            Rectangle {
                id: auraInterior

                width: 110
                height: 110

                radius: width / 2

                anchors.centerIn: parent

                color: fondo.colorAurora

                opacity: 0.15

                Behavior on color {
                    ColorAnimation {
                        duration: 500
                    }
                }
            }

            // ======================================
            // NÚCLEO CENTRAL
            // ======================================

            Rectangle {
                id: nucleoCentral

                width: 45
                height: 45

                radius: width / 2

                anchors.centerIn: parent

                color: fondo.colorAurora

                Behavior on color {
                    ColorAnimation {
                        duration: 400
                    }
                }
            }

            // ======================================
            // ANIMACIÓN
            // ======================================

            SequentialAnimation on scale {
                loops: Animation.Infinite

                NumberAnimation {
                    from: 1.0
                    to: 1.08

                    duration: 1200

                    easing.type: Easing.InOutQuad
                }

                NumberAnimation {
                    from: 1.08
                    to: 1.0

                    duration: 1200

                    easing.type: Easing.InOutQuad
                }
            }
        }

        // ==========================================
        // COMUNICACIÓN PYTHON → QML
        // ==========================================

        Connections {
            target: aurora

            function onEstadoCambiado(estado) {

                if (estado === "escuchando") {

                    estadoTexto.text = "Escuchando..."
                    fondo.colorAurora = "#3b82f6"

                } else if (estado === "procesando") {

                    estadoTexto.text = "Pensando..."
                    fondo.colorAurora = "#f59e0b"

                } else if (estado === "hablando") {

                    estadoTexto.text = "Hablando..."
                    fondo.colorAurora = "#22c55e"

                } else {

                    estadoTexto.text = "Esperando..."
                    fondo.colorAurora = "#7167ff"
                }
            }

            function onComandoCambiado(comando) {
                comandoTexto.text = comando
            }
        }

        // ==========================================
        // ÚLTIMO COMANDO
        // ==========================================

        Text {
            id: comandoTexto

            anchors.horizontalCenter: parent.horizontalCenter

            anchors.bottom: parent.bottom
            anchors.bottomMargin: 90

            text: "Decime algo..."

            color: "#66667a"

            font.pixelSize: 18

            Behavior on color {
                ColorAnimation {
                    duration: 400
                }
            }
        }

        // ==========================================
        // LÍNEA INFERIOR
        // ==========================================

        Rectangle {
            id: lineaEstado

            anchors.horizontalCenter: parent.horizontalCenter

            anchors.bottom: parent.bottom
            anchors.bottomMargin: 35

            width: 250
            height: 3

            radius: 2

            color: fondo.colorAurora

            opacity: 0.5

            Behavior on color {
                ColorAnimation {
                    duration: 400
                }
            }
        }
    }
}
