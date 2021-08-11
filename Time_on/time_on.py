import win32gui
import uiautomation as auto
import time
import datetime
import sys
import json

active_window_name = ""
start_time = datetime.datetime.now()
first_time = True


class Activities:
    def __init__(self, name, time_start, time_end):
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
        self.time = self.time_end - self.time_start

        self.total_time = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=00,
            minutes=0,
            hours=0,
            weeks=0
        )

        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        self.new = True

        with open('Time_on/activity.json', 'r') as f:
            self.data = json.load(f)

        self.recognize()

    def recognize(self):
        for i in range(0, len(self.data["Activities"])):
            if self.name == self.data["Activities"][i]["name"]:
                self.update_time(i)
                self.update_total_time(i)
                self.new = False
                break
            else:
                self.new = True
        if self.new:
            self.new_table()
            self.new = False

    def update_total_time(self, index):
        for i in range(0, len(self.data["Activities"][index]["time entries"])):

            t = datetime.datetime.strptime(self.data["Activities"][index]
                                           ["time entries"][i]["time"], '%H:%M:%S.%f')
            delta = datetime.timedelta(
                hours=t.hour, minutes=t.minute, seconds=t.second)
            self.total_time += delta

        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

        total = {
            "days": str(self.days),
            "hours": str(self.hours),
            "minutes": str(self.minutes),
            "seconds": str(self.seconds)
        }

        self.data["Activities"][index]["total time"] = total
        with open('Time_on/activity.json', 'w') as json_file:
            json.dump(self.data, json_file,
                      indent=4, sort_keys=True)

    def new_table(self):
        data = {
            "name": self.name,
            "total time": {
                "days": self.days,
                "hours": self.hours,
                "minutes": self.minutes,
                "seconds": self.seconds
            },
            "time entries": [
                {
                    "time start": str(self.time_start),
                    "time end": str(self.time_end),
                    "time": str(self.time)
                }
            ]
        }

        self.data["Activities"].append(data)
        with open('Time_on/activity.json', 'w') as json_file:
            json.dump(self.data, json_file,
                      indent=4, sort_keys=True)

    def update_time(self, index):
        time = {
            "time": str(self.time),
            "time end": str(self.time_end),
            "time start": str(self.time_start)
        }

        self.data["Activities"][index]["time entries"].append(time)
        with open('Time_on/activity.json', 'w') as json_file:
            json.dump(self.data, json_file,
                      indent=4, sort_keys=True)


def get_url():
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    name = 'https://' + edit.GetValuePattern().Value
    #name = name.split("/")
    return name


def get_window():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return active_window_name


try:
    while True:
        new_window_name = get_window()
        if 'Google Chrome' in new_window_name:
            new_window_name = new_window_name.split(" - ")
            new_window_name = new_window_name[-2]

        elif " - " in new_window_name:
            new_window_name = new_window_name.split(" - ")
            new_window_name = new_window_name[-1]

        if new_window_name != active_window_name:
            print(active_window_name)
            if not first_time:
                end_time = datetime.datetime.now()
                print(end_time-start_time)
                a = Activities(active_window_name,
                               start_time, end_time)
                start_time = datetime.datetime.now()

            first_time = False
            active_window_name = new_window_name
        time.sleep(1)

except KeyboardInterrupt:
    a = Activities(active_window_name, start_time, datetime.datetime.now())
    print("END")
