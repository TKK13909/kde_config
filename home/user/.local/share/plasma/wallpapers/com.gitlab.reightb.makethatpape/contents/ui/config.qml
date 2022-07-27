import QtQuick 2.5
import QtQuick.Dialogs 1.1 as QtDialogs
import QtQuick.Layouts 1.0
import QtQuick.Window 2.0 
import QtQuick.Controls 2.5 as QtControls
import Qt.labs.platform 1.0
//units
import org.kde.plasma.core 2.0 as Plasmacore
import org.kde.plasma.wallpapers.image 2.0 as Wallpaper
import org.kde.kquickcontrolsaddons 2.0
import org.kde.kirigami 2.5 as Kirigami

Kirigami.FormLayout  {
    id: root

    twinFormLayouts: parentLayout
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top

    property alias cfg_Image: background.source
    property string cfg_ImagePath
    property string cfg_generator
    property string cfg_preset
    property string app_name: "makethatpape"
    property string cache_path: ""
    property string path: "~/.local/share/plasma/wallpapers/com.gitlab.reightb.makethatpape/contents/scripts"
    property var options: {}
    property var option_controls
    function action_open_folder()
    {
        Qt.openUrlExternally(cache_path)
    }

    function random_hex()
    {
        return '#'+Math.floor(Math.random()*16777215).toString(16);
    }

    function validate_dependencies()
    {
        var zenity_command = `zenity --error --ellipsize --text="Error launching MakeThatPape \\nYou may be missing one of the following dependencies:\\n\\t- python3\\n\\t- PIL/pillow (pip)\\n\\t- pyopengl (pip)\\n\\t- click (pip)\\n\\nHead over to <a href=\\"https://gitlab.com/reightb/makethatpape\\">https://gitlab.com/reightb/makethatpape</a>"`
        var notify_send_command = `notify-send "Error: check https://gitlab.com/reightb/makethatpape for help"`
        main.execute(path+"/main.py -a ||" + zenity_command + "||" + notify_send_command)
    }

    function generate_presets()
    {
        var new_pre_model = []
        var i = 0
        new_pre_model[i] = {"label" : "none", "value" : "none"}
        for(var pre_key in options[cfg_generator]["presets"]){
            var value = options[cfg_generator]["presets"][pre_key]
            new_pre_model[i+=1] = {"label" : pre_key, "value" : pre_key}
        }
        presetComboBox.model = new_pre_model

    }

    function generate_options_for_generator(generator)
    {
        option_controls = {}
        optionLayout.children = ""

        generate_presets()

        for(var variable in options[generator]["variables"])
        {
            var settings = options[generator]["variables"][variable]
            var type = settings["type"]
            var default_val = ""
            if(settings["default"] !== undefined)
            {
                default_val = settings["default"]
            }
            
            if(cfg_preset in options[generator]["presets"] && variable in options[generator]["presets"][cfg_preset])
            {
                default_val = options[generator]["presets"][cfg_preset][variable]
            }

            var clean_variable = variable.replace("_", " ").replace("-", " ")
            clean_variable = clean_variable.charAt(0).toUpperCase() + clean_variable.slice(1)
            var gen_string = 'import QtQuick.Controls 2.5; import QtQuick 2.0; import QtQuick.Dialogs 1.0; import QtQuick.Layouts 1.0'
            var obj = undefined
            switch(type){
                case "color":
                gen_string += `
                    Row{         
                        spacing: 5
                        function get_value(){
                            return colorDialog.color.toString()
                        }
                        function set_value(val){
                            colorDialog.color = val
                        }
                        ColorDialog {
                            id: colorDialog
                            showAlphaChannel: false
                            title: i18nd("plasma_applet_org.kde.image", "Select Background Color")
                        }
                        Label { 
                            text: "{text}"
                        }
                        Button {
                            id: colorButton
                            width: units.gridUnit * 3
                            text: " " // needed to it gets a proper height...
                            onClicked: colorDialog.open()

                            Rectangle {
                                anchors.centerIn: parent
                                width: parent.width - 2 * units.smallSpacing
                                height: theme.mSize(theme.defaultFont).height
                                color: colorDialog.color
                            }
                        }
                        Button{
                            text: "Random"
                            onClicked: colorDialog.color = random_hex()
                        }
                    }
                `.replace("{text}", clean_variable)
                break
                case "str":
                gen_string += "Rectangle {}"
                break;
                case "int":
                var from = settings["sane_low"] ? parseInt(settings["sane_low"]) : 0
                var to = settings["sane_high"] ? parseInt(settings["sane_high"]) : 200
                gen_string += `
                    Row{
                        function get_value(){
                            return spin.value
                        }
                        function set_value(val)
                        {
                            spin.value = val
                        }
                        spacing: 10
                        Label { 
                            text: "{text}"
                        }

                        SpinBox { 
                            id: spin
                            value: {val}
                            editable: true
                            to: 1000
                            //from: {from}
                            //to: {to}
                        }
                    }
                `
            
                gen_string = gen_string.replace("{val}", default_val).replace("{text}", clean_variable).replace("{from}", from).replace("{to}", to)
                break;
            }
            var obj = Qt.createQmlObject(gen_string,
                    optionLayout, generator+"-"+variable)
            option_controls[variable] = obj
        }
        optionLayout.forceLayout()
    }

    Component.onCompleted: {
        option_controls = {}
        cache_path = StandardPaths.writableLocation(StandardPaths.GenericCacheLocation) + "/" + app_name
        cache_path = cache_path.replace("file://", "")
        validate_dependencies()
        main.execute("mkdir -p "+cache_path)
        main.execute(path+"/main.py -j", function(out){
                            var new_model = []
                            options = JSON.parse(out)
                            for(var generator in options){
                                new_model.push(generator_type(generator))
                                generate_options_for_generator(generator)
                            }
                            resizeComboBox.model = new_model
                            resizeComboBox.currentIndex = 0;

                            generate_presets()
                            restore_last_generator()
                        }, function(err){
                            main.debug("ERROR: " + err)
                        })
        supersampling.checked = wallpaper.configuration.supersampling
    }

    function restore_last_generator()
    {
        for (var i = 0; i < resizeComboBox.model.length; i++) {
            if (resizeComboBox.model[i]["value"] == wallpaper.configuration.lastGenerator) {
                resizeComboBox.currentIndex = i;
            }
        }
    }

    function generator_type(name)
    {
        return {
            "label" : i18nd('plasma_applet_org.kde.image', name[0].toUpperCase()+name.substr(1, name.length)),
            "value" : name.toLowerCase()
        }
    }

    RowLayout {
        id: mainRow
        Layout.fillWidth: true
        spacing: units.largeSpacing / 2
        QtControls.ComboBox {
            id: resizeComboBox
            property int textLength: 24
            width: theme.mSize(theme.defaultFont).width * textLength
            model: [
                generator_type("plain"),
                generator_type("grid"),
            ]

            textRole: "label"
            onCurrentIndexChanged: { 
                cfg_generator = model[currentIndex]["value"]
                generate_options_for_generator(cfg_generator)
            }
            Component.onCompleted: { // load last config
                restore_last_generator()
            }
        }
        QtControls.Label {
            text: "Presets"
        }
        QtControls.ComboBox {
            id: presetComboBox
            property int textLength: 24
            width: theme.mSize(theme.defaultFont).width * textLength
            model: [
            ]

            textRole: "label"
            onCurrentIndexChanged: { 
                cfg_preset = model[currentIndex]["value"]
                print(cfg_preset)
                print(JSON.stringify(options[cfg_generator]["presets"][cfg_preset]))
                for(var variable in options[cfg_generator]["presets"][cfg_preset])
                {

                    option_controls[variable].set_value(parseInt(options[cfg_generator]["presets"][cfg_preset][variable]))
                }

                //generate_options_for_generator(cfg_preset)
            }
            Component.onCompleted: { // load last config
                //restore_last_generator()
            }
        }

        function generate()
        {
            var final_option_map = {}
            for(var key in option_controls)
            {
                if(typeof option_controls[key]['get_value'] !== "undefined"){
                    final_option_map[key] = option_controls[key].get_value()
                }
            }

            var output_name = "output-" + cfg_generator + "-" + Math.random()*5000+".png"
            cfg_ImagePath = ""

            var w = Math.round(Screen.width) // somehow the screen width != the screen width exactly
            var h = Math.round(Screen.height)
            var command = path+"/main.py -o "+cache_path+"/" + output_name + " -g " + cfg_generator + " -s " + w + "x" + h
            for(var key in final_option_map)
            {
                //print(JSON.stringify(options[cfg_generator]))
                //print(options[cfg_generator]["presets"][cfg_preset])
                if(cfg_preset == "none" || 
                    ((cfg_preset != "none" &&
                     key in options[cfg_generator]["presets"][cfg_preset] &&
                     final_option_map[key] != options[cfg_generator]["presets"][cfg_preset][key]) || !(key in options[cfg_generator]["presets"][cfg_preset]))
                )
                {
                    command += " -p " + key + "=" + final_option_map[key] + " "
                }
            }

            if(!supersampling.checked)
            {
                command += " --disable-supersampling "
            }

            if(cfg_preset != "none")
            {
                command += " -P \"" + cfg_preset + "\""
            }

            print(command)

            wallpaper.configuration.lastGenerator = cfg_generator
            main.execute(command, function(out){
                wallpaper.configuration.wallpaperPath = ""
                wallpaper.configuration.wallpaperPath = "file:"+cache_path+"/" + output_name
                background.source = ""
                background.source = wallpaper.configuration.wallpaperPath
                var text = wallpaper.configuration.wallpaperPath
                text = text.replace("file:", "")
                cfg_Image = ""
                cfg_Image = wallpaper.configuration.wallpaperPath
                cfg_ImagePath = cfg_image
                wallpaper.configuration.generation += 1
            }, function(err){
                main.debug("ERROR: " + err)
            })
        }

        QtControls.Button {
            text: "Generate with current settings"
            onClicked: {
                mainRow.generate()
            }
        }


        QtControls.Button {
            text: "Surprise me"
            onClicked: {
                for(var key in options)
                {
                    if(key != cfg_generator){
                        continue    
                    }
                        
                    for(var opt_key in options[key]["variables"])
                    {
                        if(cfg_preset in options[key]["presets"] && opt_key in options[key]["presets"][cfg_preset])
                        {
                            option_controls[opt_key].set_value(options[key]["presets"][cfg_preset][opt_key])
                            continue
                        }
                        var opt = options[key]["variables"][opt_key]
                        var sane_min = opt["sane_low"]
                        var sane_max = opt["sane_high"]
                        var type = options[key]["variables"][opt_key]["type"]
                        
                        if(sane_min !== undefined && sane_max !== undefined)
                        {
                            var set_range = parseInt(sane_max)-parseInt(sane_min)
                            option_controls[opt_key].set_value(sane_min+Math.random()*set_range)
                        }else if(type == "color")
                        {
                            option_controls[opt_key].set_value(random_hex())
                        }
                    }

                }


                mainRow.generate()
            }
        }

        QtControls.CheckBox{
            id: supersampling
            text: "Enable supersampling"
            Component.onCompleted: { // load last config
                supersampling.checked = wallpaper.configuration.supersampling
            }
            onClicked: wallpaper.configuration.supersampling = supersampling.checked
        }
    }

    RowLayout{

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        Rectangle{
            color: "red"
            visible: false
            anchors.fill: parent
        }
        Flow {
            id: optionLayout

            anchors.fill: parent
            spacing: units.largeSpacing / 2

            anchors.margins: parent.anchors.margins
        }
    }

    RowLayout{

        MakeThatPape {
            id: main
        }

        Image{
            id: background
            smooth: true
            asynchronous: true
            fillMode: Image.PreserveAspectFit
            anchors.fill: parent
            cache: false
            visible: true
            source: wallpaper.configuration.wallpaperPath
        }

    }

    
}
