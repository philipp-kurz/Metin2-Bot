import pyautogui
import win32gui, win32ui, win32con, win32com.client
from time import sleep
import subprocess
import pygetwindow as gw
import numpy as np
import  pythoncom

# 1024 x 768


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

        pythoncom.CoInitialize()
        win32gui.ShowWindow(self.hwnd, 5)
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.hwnd)

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
        pyautogui.moveTo(self.x + x, self.y + y, duration=0.1)

    def mouse_click(self, x=None, y=None):
        sleep(0.2)
        if x is None and y is None:
            x, y = self.get_relative_mouse_pos()
        pyautogui.click(self.x + x, self.y + y, duration=0.1)

    def move_window(self, x, y):
        win32gui.MoveWindow(self.hwnd, x - 7, y, self.width, self.height, True)
        self.x, self.y = x, y

    def limit_coordinate(self, pos):
        pos = list(pos)
        if pos[0] < 0: pos[0] = 0
        elif pos[0] > self.width: pos[0] = self.width
        if pos[1] < 0: pos[1] = 0
        elif pos[1] > self.height: pos[1] = self.height
        return tuple(pos)

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

    def activate(self):
        self.mouse_move(40, -15)
        sleep(0.1)
        self.mouse_click()


class OskWindow(Window):
    def __init__(self, window_name):
        if win32gui.FindWindow(None, window_name) == 0:
            returned_value = subprocess.Popen('osk', shell=True)
            sleep(1)
        super().__init__(window_name)

        self.width, self.height = 576, 173
        self.gw_object.resizeTo(self.width, self.height)

        self.key_pos = {'space': (148, 155), 'Fn': (11, 150), '1': (55, 61), '2': (79, 67),
                        '3': (100, 65), '4': (122, 59), 'z': (67, 132), 'e': (87, 87),
                        'q': (40, 85), 'g': (134, 107), 't': (129, 86), 'Ctrl': (35, 150),
                        'h': (159, 109), 'r': (107, 88), 'f': (114, 109), 'b': (156, 134)
                        }

    def start_hitting(self):
        self.press_key(button='space', mode='down')

    def stop_hitting(self):
        self.press_key(button='space', mode='up')

    def pull_mobs(self):
        self.press_key(button='2', mode='click', count=3)

    def pick_up(self):
        self.press_key(button='z', mode='click', count=1)

    def activate_tp_ring(self):
        self.press_key(button='3', mode='click', count=1)

    def send_mount_away(self):
        self.press_key(button='Ctrl', mode='click')
        sleep(0.2)
        self.press_key(button='b', mode='click')

    def call_mount(self):
        self.press_key(button='Fn', mode='click')
        sleep(0.2)
        self.press_key(button='1', mode='click')

    def recall_mount(self):
        self.send_mount_away()
        self.un_mount()
        self.send_mount_away()
        self.call_mount()
        self.un_mount()

    def start_rotating_up(self):
        self.press_key(button='g', mode='down')

    def stop_rotating_up(self):
        self.press_key(button='g', mode='up')

    def start_rotating_down(self):
        self.press_key(button='t', mode='down')

    def stop_rotating_down(self):
        self.press_key(button='t', mode='up')

    def start_rotating_horizontally(self):
        self.press_key(button='e', mode='down')

    def stop_rotating_horizontally(self):
        self.press_key(button='e', mode='up')

    def ride_through_units(self):
        self.press_key(button='4', mode='click', count=1)

    def un_mount(self):
        self.press_key(button='Ctrl', mode='click')
        sleep(0.4)
        self.press_key(button='h', mode='click')

    def activate_aura(self):
        self.press_key(button='1', mode='click')

    def activate_berserk(self):
        self.press_key(button='2', mode='click')

    def start_zooming_out(self):
        self.press_key(button='f', mode='down')

    def stop_zooming_out(self):
        self.press_key(button='f', mode='up')

    def start_zooming_in(self):
        self.press_key(button='r', mode='down')

    def stop_zooming_in(self):
        self.press_key(button='r', mode='up')

    def press_key(self, button, mode='click', count=1):
        x, y = self.x, self.y
        if button not in self.key_pos.keys():
            raise Exception('Unknown key!')
        else:
            x += self.key_pos[button][0]
            y += self.key_pos[button][1]
            pyautogui.moveTo(x=x, y=y)
        if mode == 'click':
            for i in range(count):
                pyautogui.mouseDown()
                sleep(0.1)
                pyautogui.mouseUp()
        elif mode == 'down':
            pyautogui.mouseDown()
        elif mode == 'up':
            pyautogui.mouseUp()
