import win32gui
import win32con
import uiautomation as auto
import time
import datetime
import sys


active_window_name = ""
start_time = datetime.datetime.now()
first_time = True


def get_url():
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    name = 'https://' + edit.GetValuePattern().Value
    name = name.split("/")
    return name[2]


def get_window():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return active_window_name


while True:
    new_window_name = get_window()
    if 'Google Chrome' in new_window_name:
        new_window_name = new_window_name.split(" - ")
        new_window_name = new_window_name[-2]
        #new_window_name = get_url()

    if active_window_name != new_window_name:
        print(active_window_name)
        if not first_time:
            end_time = datetime.datetime.now()
            print(end_time-start_time)
            start_time = datetime.datetime.now()

        first_time = False
        active_window_name = new_window_name
    time.sleep(1)
