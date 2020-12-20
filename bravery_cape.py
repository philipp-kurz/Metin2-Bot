from utils.window import MetinWindow, OskWindow
import utils.utils as ut
import pyautogui
import time
import os
from tqdm import tqdm

def command_pause():
    time.sleep(0.2)


def activate_bravery_cape():
    command_pause()
    print('Pressing f2!')

def start_attacking():
    command_pause()
    print('Holding down space!')
    pyautogui.keyDown('a')


def stop_attacking():
    command_pause()
    print('Releasing space!')
    pyautogui.keyUp('space')


def rotate_view(window):
    command_pause()
    pyautogui.mouseDown(button='right', x=(653 + window.x), y=(208 + window.y), duration=0.2)
    time.sleep(1)
    pyautogui.mouseUp(button='right', duration=0.2)

    pyautogui.keyUp('w')


    # pyautogui.doubleClick(x=(653 + window.x), y=(208 + window.y))
    # window.window_click(653, 300)

def main():
    pyautogui.countdown(3)
    osk = OskWindow('On-Screen Keyboard')
    osk.move_window(x=-1495, y=810)
    aeldra = MetinWindow('Aeldra')

    for i in range(1000):
        print(f'\nIteration {i}:')

        print('pulling mobs')
        command_pause()
        osk.pull_mobs()

        print('start hitting')
        osk.start_hitting()
        command_pause()

        print('Kill mobs')
        time.sleep(7)

        print('stop hitting')
        osk.stop_hitting()
        command_pause()

        print('picking up')
        osk.pick_up()
        command_pause()

    print('Done')


if __name__ == '__main__':
    # utils.countdown()
    main()

