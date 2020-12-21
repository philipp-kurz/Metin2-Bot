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
    smFilter = SnowManFilter()
    cascade_snowmen = cv.CascadeClassifier('cascade/cascade.xml')

    while True:
        loop_time = time.time()
        screenshot = aeldra.capture()

        processed_screenshot = vision.apply_hsv_filter(screenshot, hsv_filter=smFilter)

        rectangles = cascade_snowmen.detectMultiScale(processed_screenshot)

        original_detected = vision.draw_rectangles(processed_screenshot, rectangles)

        cv.imshow('Video Feed', original_detected)
        print(f'{round(1 / (time.time() - loop_time),2)} FPS')

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    main()

