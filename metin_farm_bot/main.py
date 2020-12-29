import cv2 as cv
import utils
from captureAndDetect import CaptureAndDetect
from utils.window import MetinWindow
from bot import MetinFarmBot
import tkinter as tk
from utils import SnowManFilter, SnowManFilterRedForest
from functools import partial


def main():

    # Choose which metin
    metin_selection = {'metin': None}
    metin_select(metin_selection)
    metin_selection = metin_selection['metin']
    hsv_filter = SnowManFilter() if metin_selection != 'lv_90' else SnowManFilterRedForest()

    # Countdown
    utils.countdown()

    # Get window and start window capture
    metin_window = MetinWindow('Aeldra')

    capt_detect = CaptureAndDetect(metin_window, 'classifier/cascade/cascade.xml', hsv_filter)

    # Initialize the bot
    bot = MetinFarmBot(metin_window, metin_selection)
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

def metin_select(metin_selection):
    metins = {'Lvl. 40: Tal von Seungryong': 'lv_40',
              'Lvl. 60: Hwang-Tempel': 'lv_60',
              'Lvl. 70: Feuerland': 'lv_70',
              'Lvl. 90: Roter Wald': 'lv_90'}

    def set_metin_cb(window, metin, metin_selection):
        metin_selection['metin'] = metin
        window.destroy()

    window = tk.Tk()
    window.title("Metin2 Bot")
    tk.Label(window, text='Select Metin:').pack(pady=5)

    for button_text, label in metins.items():
        tk.Button(window, text=button_text, width=30, command=partial(set_metin_cb, window, label, metin_selection))\
            .pack(padx=3, pady=3)

    window.mainloop()

if __name__ == '__main__':
    main()
