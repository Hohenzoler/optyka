import os.path
import json

settings = {'WIDTH': 1000, 'HEIGHT': 700, 'FULLSCREEN': 'OFF', 'HOTBAR_POSITION': 'bottom', 'VSYNC': 'OFF', 'DEBUG': 'True', 'Flashlight_FOV': 5, 'Flashlight_Rays': 15, 'HD_Flashlight': 'ON'}

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
    with open(js, 'r') as f:
        json_object = json.loads(f.read())
        f.close()
    s = json_object
    return s

def writesettingstofile(s, i=1, js='settings.json'): #funkcja zapisuje ustawienia do pilku
    json_string = json.dumps(s, indent=i)
    with open(js, 'w') as f:
        f.write(json_string)
        f.close()