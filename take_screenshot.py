import os
import pyautogui
from datetime import datetime


def capture_image() -> dict :

    file_name = f'Screenshot {datetime.today().strftime('%Y-%m-%d %H%M%S')}.png'
    path = r'static/image'

    if not os.path.exists(path):
        os.mkdir(path)

    full_path = os.path.join(path, file_name)
    img = pyautogui.screenshot()
    img.save(full_path)

    return {'screenshot': f'static/image/{file_name}'}

