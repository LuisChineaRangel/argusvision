pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import "components"

ApplicationWindow {
    id: window
    visible: true
    visibility: Window.Maximized
    width: 1100
    height: 800
    title: "ArgusVision"
    color: Theme.background

    required property var view_bridge
    property var bridge: window.view_bridge

    Shortcut {
        sequence: "Escape"
        onActivated: Qt.quit()
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: Theme.background

            Image {
                id: videoStream
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                source: "image://video/frame"
                cache: false

                // Trigger refresh when the bridge emits a signal
                Connections {
                    target: window.bridge
                    function onFrameUpdated() {
                        videoStream.source = "image://video/frame?" + Math.random()
                    }
                }
            }
        }

        Rectangle {
            Layout.preferredWidth: Theme.sidebarWidth
            Layout.fillHeight: true
            color: Theme.panel

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.paddingLarge
                spacing: Theme.spacing

                Column {
                    Layout.fillWidth: true
                    Layout.topMargin: 15
                    spacing: 5

                    Text {
                        text: "ArgusVision"
                        color: Theme.primary
                        font.pixelSize: Theme.fontSizeHeader
                        font.bold: true
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    Text {
                        text: "Tracking System"
                        color: Theme.textDim
                        font.pixelSize: Theme.fontSizeTitle
                        font.bold: true
                        font.letterSpacing: 4
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }

                InfoCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    title: "System Performance"
                    value: window.bridge.fps + " FPS"
                    valueColor: window.bridge.fps > 25 ? Theme.success : Theme.secondary
                }

                InfoCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    title: "Active Fingers"
                    value: window.bridge.fingers
                }

                InfoCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    title: "Detected Hands"
                    value: window.bridge.hands
                }

                GestureList {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    gestures: window.bridge.gestures
                }

                Button {
                    id: terminateBtn
                    text: "TERMINATE SESSION"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50

                    contentItem: Text {
                        text: terminateBtn.text
                        color: terminateBtn.hovered ? "white" : Theme.secondary
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        color: terminateBtn.hovered ? Theme.secondary : "transparent"
                        border.color: Theme.secondary
                        border.width: 2
                        radius: 10
                    }

                    onClicked: Qt.quit()
                }
            }
        }
    }
}
