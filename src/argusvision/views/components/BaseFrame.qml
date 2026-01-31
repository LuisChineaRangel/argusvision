import QtQuick
import QtQuick.Effects

Rectangle {
    id: root
    property alias content: contentLoader.sourceComponent

    color: Theme.surface
    radius: Theme.cardRadius
    border.color: Theme.panel
    border.width: 1

    layer.enabled: true
    layer.effect: MultiEffect {
        shadowEnabled: true
        shadowBlur: 0.8
        shadowVerticalOffset: 4
        shadowColor: "black"
        shadowOpacity: 0.3
    }

    Loader {
        id: contentLoader
        anchors.fill: parent
        anchors.margins: Theme.paddingMedium
    }
}
