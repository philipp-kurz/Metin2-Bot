import pyautogui
import win32gui
from time import sleep
import subprocess


class Window:
    def __init__(self, window_name):
        self.name = window_name
        self.hwnd = win32gui.FindWindow(None, window_name)
        if self.hwnd == 0:
            raise Exception(f'Window "{self.name}" not found!')

        rect = win32gui.GetWindowRect(self.hwnd)
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2] - self.x
        self.height = rect[3] - self.y

        win32gui.ShowWindow(self.hwnd, 5)
        pyautogui.moveTo(self.x + 20, self.y + 5, duration=0.3)
        sleep(0.1)
        pyautogui.click()

    def print_relative_mouse_pos(self, loop=False):
        repeat = True
        while repeat:
            repeat = loop
            curr_x, curr_y = pyautogui.position()
            print(curr_x - self.x, curr_y - self.y)
            if loop:
                sleep(1)

    def window_click(self, x, y):
        sleep(0.2)
        pyautogui.click(self.x + x, self.y + y, duration=0.3)

    def move_window(self, x, y):
        win32gui.MoveWindow(self.hwnd, x - 7, y, self.width, self.height, True)
        self.x, self.y = x, y


class MetinWindow(Window):
    def __init__(self, window_name):
        super().__init__(window_name)


class OskWindow(Window):
    def __init__(self, window_name):
        if win32gui.FindWindow(None, window_name) == 0:
            returned_value = subprocess.Popen('osk', shell=True)
            sleep(1)
        super().__init__(window_name)

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
