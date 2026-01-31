pragma Singleton
import QtQuick

QtObject {
    // Colors
    readonly property color primary: "#00ffcc"
    readonly property color secondary: "#ff5252"
    readonly property color success: "#4caf50"
    readonly property color background: "#121212"
    readonly property color surface: "#1e1e1e"
    readonly property color panel: "#1a1a1a"

    // Text Colors
    readonly property color textMain: "#ffffff"
    readonly property color textDim: "#888888"

    // Fonts
    readonly property string fontFamily: "Segoe UI"
    readonly property int fontSizeHeader: 32
    readonly property int fontSizeTitle: 10
    readonly property int fontSizeValue: 28
    readonly property int fontSizeBody: 14

    // Dimensions
    readonly property int paddingLarge: 25
    readonly property int paddingMedium: 15
    readonly property int spacing: 25
    readonly property int cardRadius: 12
    readonly property int sidebarWidth: 340
}
