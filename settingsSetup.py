import os.path
import json

settings = {'WIDTH': 1000, 'HEIGHT': 700, 'FULLSCREEN': 'OFF', 'HOTBAR_POSITION': 'bottom', 'VSYNC': 'OFF', 'DEBUG': 'False', 'Flashlight_FOV': 20, 'Flashlight_Rays': 30, 'Flashlight_Depth': 500, "HD_Flashlight": "OFF"}

def start(s=settings):
    if os.path.exists('settings.json'):
        try: #sprawdza czy z pliku mozna wydostac json
            json_object = load_settings()
        except:
            writesettingstofile(s)
            return s

        if len(json_object) == len(settings):
            s = json_object
        else:
            s.update(json_object)
            writesettingstofile(s)
    else:
        writesettingstofile(s)
    return s

def load_settings(js='settings.json'): #czyta ustawienia z pliku
    try:
        with open(js, 'r') as f:
            json_object = json.loads(f.read())
            f.close()
        s = json_object
        return s
    except:
        return {}

def writesettingstofile(s, i=1, js='settings.json'): #funkcja zapisuje ustawienia do pilku
        json_string = json.dumps(s, indent=i)
        with open(js, 'w') as f:
            f.write(json_string)
            f.close()