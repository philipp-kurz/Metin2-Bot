from utils.window import MetinWindow, OskWindow
import pyautogui
import time
import cv2 as cv
from utils.vision import Vision, MobInfoFilter
import pytesseract
import re



def command_pause():
    time.sleep(0.2)


def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pyautogui.countdown(3)
    aeldra = MetinWindow('Aeldra')
    vision = Vision()
    # vision.init_control_gui()

    mi_filter = MobInfoFilter()

    while True:
        loop_time = time.time()
        # Get full image
        img = aeldra.capture()
        # img = cv.imread('OCR/Mob_info.jpg')

        # pos = aeldra.get_relative_mouse_pos()
        # width = 200
        # height
        # top_left = (int(pos[0] - width / 2),

        # Crop section
        img = vision.extract_section(img, (300, 21), (560, 37))

        # Apply HSV filter
        img = vision.apply_hsv_filter(img, hsv_filter=mi_filter)
        cv.imshow('Image', img)

        text = pytesseract.image_to_string(img)
        print(process_metin_info(text))

        print(f'{round(1 / (time.time() - loop_time), 2)} FPS')
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break

    print('Done')

def process_metin_info(text):
    # Remove certain substrings
    remove = ['\f', '.', '°', '%', '‘', ',']
    for char in remove:
        text = text.replace(char, '')

    # Replace certain substrings
    replace = [('\n', ' '), ('Lw', 'Lv'), ('Lv', 'Lv.')]
    for before, after in replace:
        text = text.replace(before, after)

    # '%' falsely detected as '96'
    p = re.compile('(?<=\d)96')
    m = p.search(text)
    if m:
        span = m.span()
        text = text[:span[0]]

    # Parse the string
    parts = text.split()
    parts = [part for part in parts if len(part) > 0]

    if len(parts) == 0:
        return None
    else:
        health = int(re.sub('[^0-9]', '', parts[-1]))
        name = ' '.join(parts[:-1])
        return name, health

if __name__ == '__main__':
    main()


