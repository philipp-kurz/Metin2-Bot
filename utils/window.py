import pyautogui
import win32gui, win32ui, win32con
from time import sleep
import subprocess
import pygetwindow as gw
import numpy as np


class Window:
    def __init__(self, window_name):
        self.name = window_name
        self.hwnd = win32gui.FindWindow(None, window_name)
        if self.hwnd == 0:
            raise Exception(f'Window "{self.name}" not found!')

        self.gw_object = gw.getWindowsWithTitle(self.name)[0]

        rect = win32gui.GetWindowRect(self.hwnd)
        border = 8
        title_bar = 31
        self.x = rect[0] + border
        self.y = rect[1] + title_bar
        self.width = rect[2] - self.x - border
        self.height = rect[3] - self.y - border

        self.cropped_x = border
        self.cropped_y = title_bar

        win32gui.ShowWindow(self.hwnd, 5)
        win32gui.SetForegroundWindow(self.hwnd)
        # pyautogui.moveTo(self.x + 20, self.y + 5, duration=0.3)
        # sleep(0.1)
        # pyautogui.click()

    def get_relative_mouse_pos(self):
        curr_x, curr_y = pyautogui.position()
        return curr_x - self.x, curr_y - self.y

    def print_relative_mouse_pos(self, loop=False):
        repeat = True
        while repeat:
            repeat = loop
            print(self.get_relative_mouse_pos)
            if loop:
                sleep(1)

    def mouse_move(self, x, y):
        sleep(0.2)
        pyautogui.moveTo(self.x + x, self.y + y, duration=0.3)

    def mouse_click(self, x, y):
        sleep(0.2)
        pyautogui.click(self.x + x, self.y + y, duration=0.3)

    def move_window(self, x, y):
        win32gui.MoveWindow(self.hwnd, x - 7, y, self.width, self.height, True)
        self.x, self.y = x, y

    def capture(self):
        # https://stackoverflow.com/questions/6312627/windows-7-how-to-bring-a-window-to-the-front-no-matter-what-other-window-has-fo
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.width, self.height), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        # https://stackoverflow.com/questions/41785831/how-to-optimize-conversion-from-pycbitmap-to-opencv-image
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Drop the alpha channel
        img = img[..., :3]

        # make image C_CONTIGUOUS
        img = np.ascontiguousarray(img)

        return img


class MetinWindow(Window):
    def __init__(self, window_name):
        super().__init__(window_name)


class OskWindow(Window):
    def __init__(self, window_name):
        if win32gui.FindWindow(None, window_name) == 0:
            returned_value = subprocess.Popen('osk', shell=True)
            sleep(1)
        super().__init__(window_name)

        self.width, self.height = 576, 173
        self.gw_object.resizeTo(self.width, self.height)

        self.key_pos = {'space': (148, 155),    'Fn': (11, 150),    '1': (55, 61),      '2': (79, 67),
                        '3': (100, 65),         '4': (122, 59),     'z': (67, 132),     'e': (87, 87),
                        'q': (40, 85),          'g': (134, 107),    't': (129, 86),     'Ctrl': (35, 150),
                        'h': (159, 109),
                        }

    def start_hitting(self):
        self.press_key(button='space', mode='down')

    def stop_hitting(self):
        self.press_key(button='space', mode='up')

    def pull_mobs(self):
        self.press_key(button='2', mode='click', count=3)

    def pick_up(self):
        self.press_key(button='z', mode='click', count=1)

    def press_key(self, button, mode='click', count=1):
        x, y = self.x, self.y
        if button not in self.key_pos.keys():
            raise Exception('Unknown key!')
        else:
            x += self.key_pos[button][0]
            y += self.key_pos[button][1]
        if mode == 'click':
            for i in range(count):
                pyautogui.mouseDown(x=x, y=y, duration=0.2)
                sleep(0.1)
                pyautogui.mouseUp()
        elif mode == 'down':
            pyautogui.mouseDown(x=x, y=y, duration=0.2)
        elif mode == 'up':
            pyautogui.mouseUp(x=x, y=y)
