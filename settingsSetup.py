import os.path
import json

settings = {'WIDTH': 1200, 'HEIGHT': 700, 'HOTBAR_POSITION': 'buttom'}


def start(s=settings):
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            json_object = json.loads(f.read())
            f.close()
        s = json_object

    else:
        json_string = json.dumps(s, indent=1)
        with open('settings.json', 'w') as f:
            f.write(json_string)
            f.close()
    return s
