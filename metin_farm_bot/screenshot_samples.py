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
    # vision.init_control_gui()
    sm_filter = SnowManFilter()

    count = {'p': 0, 'n': 0}

    while True:
        loop_time = time.time()
        screenshot = aeldra.capture()

        processed_screenshot = vision.apply_hsv_filter(screenshot, hsv_filter=sm_filter)

        cv.imshow('Video Feed', processed_screenshot)
        # print(f'{round(1 / (time.time() - loop_time),2)} FPS')

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break
        elif key == ord('p'):
            cv.imwrite('classifier/positive_2020_12_22_01/{}.jpg'.format(int(loop_time)), processed_screenshot)
            count['p'] += 1
            print(f'Saved positive sample. {count["p"]} total.')
        elif key == ord('n'):
            cv.imwrite('classifier/negative_2020_12_22_01/{}.jpg'.format(int(loop_time)), processed_screenshot)
            count['n'] += 1
            print(f'Saved negative sample. {count["n"]} total.')


if __name__ == '__main__':
    main()

