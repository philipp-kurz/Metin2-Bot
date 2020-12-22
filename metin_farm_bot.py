from utils.window import MetinWindow, OskWindow
import pyautogui
import time
import cv2 as cv
from utils.vision import Vision, SnowManFilter
import numpy as np



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

        # Take screenshot of client window and process it
        screenshot = aeldra.capture()
        processed_screenshot = vision.apply_hsv_filter(screenshot, hsv_filter=sm_filter)
        vision.black_out_area(processed_screenshot, (441, 325), (581, 461))  # Remove player

        # Detect snowmen on the screenshot
        rectangles = cascade_snowmen.detectMultiScale2(processed_screenshot)

        # If matches were found
        if len(rectangles[0]) > 0:
            # Get best match
            best_match = rectangles[0][np.argmax(rectangles[1])]

            # Draw bounding boxes
            img = screenshot
            vision.draw_rectangles(img, rectangles[0])
            vision.draw_rectangles(img, [best_match], bgr_color=(0, 0, 255))

            click_pos = (int(best_match[0] + best_match[2] / 2), int(best_match[1] + best_match[3] / 2))
            vision.draw_marker(img, click_pos)
            aeldra.mouse_move(*click_pos)

            pos = aeldra.get_relative_mouse_pos()
            width = 200
            height = 150
            top_left = (int(pos[0] - width/2), pos[1] - height)
            bottom_right = (int(pos[0] + width / 2), pos[1])
            rect = (top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
            vision.draw_rectangles(img, [rect])
            mob_title_box = aeldra.capture()
            mob_title_box = vision.extract_section(mob_title_box, top_left, bottom_right)

            match_loc = vision.template_match_alpha(mob_title_box, 'utils/needle_metin.png')


            if match_loc is not None:
                vision.draw_marker(mob_title_box, match_loc)
                pyautogui.click()


        # Display
        cv.imshow('Video Feed', img)
        print(f'{round(1 / (time.time() - loop_time),2)} FPS')

        # Quit if necessary
        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break


if __name__ == '__main__':
    main()

