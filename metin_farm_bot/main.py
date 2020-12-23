import cv2 as cv
import utils
from captureAndDetect import CaptureAndDetect
from utils.window import MetinWindow
from bot import MetinFarmBot


def main():
    utils.countdown()
    # Get window and start window capture
    metin_window = MetinWindow('Aeldra')

    capt_detect = CaptureAndDetect(metin_window, 'classifier/cascade/cascade.xml')

    # Initialize the bot
    bot = MetinFarmBot(metin_window)
    capt_detect.start()
    bot.start()

    while True:

        # Get new detections
        screenshot, screenshot_time, detection, detection_time, detection_image = capt_detect.get_info()

        # Update bot with new image
        bot.detection_info_update(screenshot, screenshot_time, detection, detection_time)

        if detection_image is None:
            continue

        # Draw bot state on image
        overlay_image = bot.get_overlay_image()
        detection_image = cv.addWeighted(detection_image, 1, overlay_image, 1, 0)

        # Display image
        cv.imshow('Matches', detection_image)

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        key = cv.waitKey(1)

        if key == ord('q'):
            capt_detect.stop()
            bot.stop()
            cv.destroyAllWindows()
            break

    print('Done.')


if __name__ == '__main__':
    main()
