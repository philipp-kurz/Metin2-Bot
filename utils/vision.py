# Mostly copied from https://github.com/learncodebygaming/opencv_tutorials/blob/master/006_hsv_thresholding/vision.py
import cv2 as cv
import numpy as np
import os


class HsvFilter:
    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None,
                    sAdd=None, sSub=None, vAdd=None, vSub=None):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub


class SnowManFilter(HsvFilter):
    def __init__(self):
        self.hMin = 106
        self.sMin = 0
        self.vMin = 0
        self.hMax = 116
        self.sMax = 90
        self.vMax = 255
        self.sAdd = 0
        self.sSub = 0
        self.vAdd = 255
        self.vSub = 0


class MobInfoFilter(HsvFilter):
    def __init__(self):
        self.hMin = 0
        self.sMin = 0
        self.vMin = 0
        self.hMax = 179
        self.sMax = 25
        self.vMax = 255
        self.sAdd = 0
        self.sSub = 0
        self.vAdd = 0
        self.vSub = 0


class Vision:
    TRACKBAR_WINDOW = "Trackbars"

    def __init__(self, needle_img_path=None, method=cv.TM_CCOEFF_NORMED):
        # # load the image we're trying to match
        # # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        # # self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        #
        # # Save the dimensions of the needle image
        # self.needle_w = self.needle_img.shape[1]
        # self.needle_h = self.needle_img.shape[0]
        #
        # # There are 6 methods to choose from:
        # # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        # self.method = method
        pass

    # create gui window with controls for adjusting arguments in real-time
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    # returns an HSV filter object based on the control GUI values
    def get_hsv_filter_from_controls(self):
        # Get current positions of all trackbars
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter

    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c

    def draw_marker(self, img, position, bgr_color=(255, 0, 0)):
        cv.drawMarker(img, position, color=bgr_color, markerType=cv.MARKER_CROSS, thickness=2)

    def draw_rectangles(self, haystack_img, rectangles, bgr_color=(0, 255, 0)):
        for (x, y, w, h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, bgr_color, lineType=cv.LINE_4)


    def add_rectangles_to_image(self, image, rectangles):
        if len(rectangles > 0):
            image_with_matches = self.draw_rectangles(image, [rectangles[0]], bgr_color=(0, 0, 255))
            if len(rectangles > 1):
                image_with_matches = self.draw_rectangles(image, rectangles[1:])
        return image

    def black_out_area(self, image, top_left, bottom_right):
        cv.rectangle(image, top_left, bottom_right, (0, 0, 0), cv.FILLED)
        # cv.rectangle(image, top_left, bottom_right, (255, 0, 0), cv.LINE_4)

    def extract_section(self, image, top_left, bottom_right):
        return image[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]

    def template_match_alpha(self, haystack_img, needle_path):
        needle = cv.imread(needle_path, cv.IMREAD_UNCHANGED)
        result = cv.matchTemplate(haystack_img, needle[:, :, :3], cv.TM_SQDIFF, mask=needle[:, :, 3])
        match_val, _, match_loc, _ = cv.minMaxLoc(result)
        if match_val > 10_000:
            return None
        else:
            return match_loc

