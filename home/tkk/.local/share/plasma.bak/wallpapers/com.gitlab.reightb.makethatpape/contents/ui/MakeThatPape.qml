import QtQuick 2.0
import QtQuick.Layouts 1.1
import QtQuick.Controls 2.2

import org.kde.plasma.components 2.0 as PlasmaComponents
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kquickcontrolsaddons 2.0
Item {
    id: main

    function debug(text)
    {
        execute("notify-send '" + text + "'")
    }
    function execute(program, callback)
    {
        executable.exec(program, callback)
    }

    PlasmaCore.DataSource {
        id: executable
        engine: "executable"
        connectedSources: []
        property var callbacks: ({})
        property var error_callbacks: ({})
        onNewData: {
            var stdout = data["stdout"]
            var stderr = data["stderr"]
         
            console.log(sourceName)
            console.log(JSON.stringify(data))

            try{
                if (callbacks[sourceName] !== undefined) 
                {
                    callbacks[sourceName](stdout);
                }
                if(error_callbacks[sourceName] !== undefined)
                {
                    error_callbacks[sourceName](stdout);
                }
            }catch(err){
                console.log("error: " + err.message)
            }
   
            disconnectSource(sourceName)
        }
        
        function exec(cmd, onNewDataCallback, onNewErrorCallback) {
            if (onNewDataCallback !== undefined){
                callbacks[cmd] = onNewDataCallback
            }
            if (onNewErrorCallback !== undefined){
                error_callbacks[cmd] = onNewErrorCallback
            }

            console.log("Calling " + cmd)
            connectSource(cmd)
        }

    }
}
