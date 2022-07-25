import QtQuick 2.5
import org.kde.plasma.wallpapers.image 2.0 as Wallpaper
import org.kde.plasma.core 2.0 as PlasmaCore

Image{
    id: background
    anchors.fill: parent
    fillMode: Image.PreserveAspectCrop
    source: wallpaper.configuration.wallpaperPath
}


