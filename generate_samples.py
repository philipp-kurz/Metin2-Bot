from utils.window import MetinWindow, OskWindow
import pyautogui
import time
import cv2 as cv
from utils.vision import Vision, SnowManFilter


def command_pause():
    time.sleep(0.2)


def main():
    pyautogui.countdown(3)
    aeldra = MetinWindow('Aeldra')
    vision = Vision()
    vision.init_control_gui()
    smFilter = SnowManFilter()

    while True:
        loop_time = time.time()
        screenshot = aeldra.capture()

        processed_screenshot = vision.apply_hsv_filter(screenshot)#, hsv_filter=smFilter)
        cv.imshow('Video Feed', processed_screenshot)
        print(f'{round(1 / (time.time() - loop_time),2)} FPS')

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break
        elif key == ord('p'):
            cv.imwrite('positive/{}.jpg'.format(int(loop_time)), processed_screenshot)
        elif key == ord('n'):
            cv.imwrite('negative/{}.jpg'.format(int(loop_time)), processed_screenshot)


if __name__ == '__main__':
    main()

