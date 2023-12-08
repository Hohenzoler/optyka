import os.path

def start():
    settings = []

    if os.path.exists('settings.ini'):
        with open('settings.ini', 'r') as f:
            for row in f:
                s = row.split('=', 1)[1].strip()
                settings.append(s)
        f.close()
    else:
        with open("settings.txt", 'a') as f:
            f.write('WIDTH=1000\n')
            f.write('HEIGHT=700\n')
            f.write('POSITION=buttom\n')
            f.close()
        settings.append(1000)
        settings.append(700)
        settings.append('buttom')
    return settings
