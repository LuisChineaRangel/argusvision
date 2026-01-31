pragma ComponentBehavior: Bound
import QtQuick

BaseFrame {
    id: info
    property string title: "TITLE"
    property string value: "--"
    property color valueColor: Theme.primary

    content: Column {
        spacing: 5

        Text {
            text: info.title.toUpperCase()
            font.pixelSize: Theme.fontSizeTitle
            font.bold: true
            color: Theme.textDim
            font.letterSpacing: 1
        }

        Text {
            text: info.value
            font.pixelSize: Theme.fontSizeValue
            font.bold: true
            color: info.valueColor
        }
    }
}
