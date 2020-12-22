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
    sm_filter = SnowManFilter()

    cascade_snowmen = cv.CascadeClassifier('classifier/cascade/cascade.xml')

    while True:
        loop_time = time.time()
        screenshot = aeldra.capture()

        processed_screenshot = vision.apply_hsv_filter(screenshot, hsv_filter=sm_filter)

        vision.black_out_area(processed_screenshot, (441, 325), (581, 461))  # Remove player

        rectangles = cascade_snowmen.detectMultiScale(processed_screenshot)

        image_with_matches = screenshot
        vision.draw_rectangles(image_with_matches, rectangles)

        cv.imshow('Video Feed', image_with_matches)
        print(f'{round(1 / (time.time() - loop_time),2)} FPS')

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    main()

