import QtQuick 2.0
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.components 3.0 as PlasmaComponents3

MouseArea {
	id: sectionDelegate

	width: ListView.view.width
	// height: childrenRect.height
	implicitHeight: listView.iconSize

	property bool enableJumpToSection: false

	PlasmaComponents3.Label {
		id: sectionHeading
		anchors {
			left: parent.left
			leftMargin: PlasmaCore.Units.smallSpacing
			verticalCenter:  parent.verticalCenter
		}
		text: {
			if (section == appsModel.recentAppsSectionKey) {
				return appsModel.recentAppsSectionLabel
			} else {
				return section
			}
		}

		// Add 4pt to font. Default 10pt => 14pt
		font.pointSize: PlasmaCore.Theme.defaultFont.pointSize + 4

		property bool centerOverIcon: sectionHeading.contentWidth <= listView.iconSize
		width: centerOverIcon ? listView.iconSize : parent.width
		horizontalAlignment: centerOverIcon ? Text.AlignHCenter : Text.AlignLeft
	}

	HoverOutlineEffect {
		id: hoverOutlineEffect
		anchors.fill: parent
		visible: enableJumpToSection && mouseArea.containsMouse
		hoverRadius: width/2
		pressedRadius: width
		mouseArea: sectionDelegate
	}

	hoverEnabled: true
	onClicked: {
		if (enableJumpToSection) {
			if (appsModel.order == "alphabetical") {
				jumpToLetterView.show()
			} else { // appsModel.order = "categories"
				jumpToLetterView.show()
			}
		}
	}
}
