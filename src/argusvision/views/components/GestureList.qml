pragma ComponentBehavior: Bound
import QtQuick

BaseFrame {
    id: gesturesList
    property var gestures: []

    content: Column {
        spacing: 10

        Text {
            text: "DETECTED GESTURES"
            font.pixelSize: Theme.fontSizeTitle
            font.bold: true
            color: Theme.textDim
            font.letterSpacing: 1
        }

        Column {
            spacing: 5
            Repeater {
                model: gesturesList.gestures
                delegate: Text {
                    required property string modelData
                    text: "• " + modelData
                    font.pixelSize: Theme.fontSizeBody
                    color: Theme.primary
                }
            }
        }
    }
}
