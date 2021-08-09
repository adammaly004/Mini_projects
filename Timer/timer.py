from tkinter import *
from tkinter import ttk
from pygame import mixer

WIDTH = 800
HEIGHT = 500

mixer.init()  # initialise the pygame


class App():
    def __init__(self, master):
        self.master = master
        self.master.config(bg="white")
        self.master.geometry(f'{WIDTH}x{HEIGHT}+500+200')
        self.master.resizable(width=False, height=False)
        self.master.title('Timer')

        self.max_time = 25*60
        self.max_pause = 5*60
        self.time = self.max_time
        self.running = False
        self.pause = False

        self.draw_window()
        self.show_time()

    def draw_window(self):
        self.label = Label(self.master, text="",
                           font=("Helvetice", 80), bg="white")
        self.label.place(x=400, y=150, anchor="center")

        self.progressbar = ttk.Progressbar(
            self.master, orient='horizontal', mode='determinate', length=400)
        self.progressbar["value"] = 100
        self.progressbar.place(x=400, y=230, anchor="center")

        self.start_btn = Button(self.master, text="start",
                                command=self.run, font=("Helvetice", 15), height=1, width=10)
        self.start_btn.place(x=WIDTH/3, y=300, anchor="center")

        self.reset_btn = Button(self.master, text="reset", command=self.reset, font=(
            "Helvetice", 15), height=1, width=10)
        self.reset_btn.place(x=WIDTH/3*2, y=300, anchor="center")

        self.set_btn = Button(self.master, text="set timer", command=self.set_timer, font=(
            "Helvetice", 15), height=1, width=10)
        self.set_btn.place(x=WIDTH/2, y=350, anchor="center")

    def couldown(self):
        if self.running:
            self.time -= 1
            self.repetition_intervals()
            self.update_progressbar()
            self.show_time()
            self.label.after(1000, self.couldown)

    def repetition_intervals(self):
        if self.pause:
            if self.time <= 0:
                self.time = self.max_time
                self.sound()
                self.pause = False

        else:
            if self.time <= 0:
                self.time = self.max_pause
                self.sound()
                self.pause = True

    def show_time(self):
        self.mins, self.secs = divmod(self.time, 60)
        self.hour, self.mins = divmod(self.mins, 60)

        if self.mins < 10:
            self.mins = "0" + str(self.mins)
        if self.hour < 10:
            self.hour = "0" + str(self.hour)
        if self.secs < 10:
            self.secs = "0" + str(self.secs)

        self.label.configure(text=f"{self.hour}:{self.mins}:{self.secs}")

    def update_progressbar(self):
        if self.pause:
            self.progressbar["value"] = self.time * 100 / self.max_pause
        else:
            self.progressbar["value"] = self.time * 100 / self.max_time

    def run(self):
        if not self.running:
            self.running = True
            self.couldown()

    def reset(self):
        self.pause = False
        self.running = False
        self.time = self.max_time
        self.progressbar["value"] = 100
        self.show_time()

    def set_timer(self):
        self.master2 = Toplevel(self.master)
        self.master2.config(bg="white")
        self.master2.geometry(
            f"400x250+{root.winfo_x() + WIDTH - 600}+{root.winfo_y() + HEIGHT - 375}")
        self.master2.resizable(width=False, height=False)
        self.master2.title("Timer setting")

        self.time_in_entry()
        self.draw_set_timer()

    def change_time(self):
        self.time = int(self.hours.get())*3600 + \
            int(self.minutes.get())*60 + int(self.seconds.get())

        self.pause = int(self.pause_hours.get())*3600 + \
            int(self.pause_minutes.get())*60 + int(self.pause_seconds.get())

        self.max_time = self.time
        self.max_pause = self.pause
        self.show_time()
        self.reset()
        self.master2.destroy()

    def draw_set_timer(self):
        # Interval
        self.interval_label = Label(self.master2, text="Interval time",
                                    font=("Helvetice", 15), bg="white")
        self.interval_label.place(x=200, y=10, anchor="center")

        self.hour_entry = Entry(self.master2, width=3, font=("Arial", 18, ""),
                                textvariable=self.hours)
        self.hour_entry.place(x=400/3, y=50, anchor="center")
        self.minute_entry = Entry(self.master2, width=3, font=("Arial", 18, ""),
                                  textvariable=self.minutes)
        self.minute_entry.place(x=400/2, y=50, anchor="center")
        self.second_entry = Entry(self.master2, width=3, font=("Arial", 18, ""),
                                  textvariable=self.seconds)
        self.second_entry.place(x=400/3*2, y=50, anchor="center")

        # Pause
        self.pause_label = Label(self.master2, text="Pause time",
                                 font=("Helvetice", 15), bg="white")
        self.pause_label.place(x=200, y=90, anchor="center")

        self.pause_hour_entry = Entry(self.master2, width=3, font=("Arial", 18, ""),
                                      textvariable=self.pause_hours)
        self.pause_hour_entry.place(x=400/3, y=130, anchor="center")
        self.pause_minute_entry = Entry(self.master2, width=3, font=("Arial", 18, ""),
                                        textvariable=self.pause_minutes)
        self.pause_minute_entry.place(x=400/2, y=130, anchor="center")
        self.pause_second_entry = Entry(self.master2, width=3, font=("Arial", 18, ""),
                                        textvariable=self.pause_seconds)
        self.pause_second_entry.place(x=400/3*2, y=130, anchor="center")
        self.submit_btn = Button(self.master2, text="Submit",
                                 command=self.change_time, font=("Helvetice", 15), height=1, width=10)
        self.submit_btn.place(x=200, y=200, anchor="center")

    def time_in_entry(self):
        self.minutes = StringVar()
        self.hours = StringVar()
        self.seconds = StringVar()

        self.max_mins, self.max_secs = divmod(self.max_time, 60)
        self.max_hour, self.mins = divmod(self.max_mins, 60)

        if self.max_mins < 10:
            self.max_mins = "0" + str(self.max_mins)
        if self.max_hour < 10:
            self.max_hour = "0" + str(self.max_hour)
        if self.max_secs < 10:
            self.max_secs = "0" + str(self.max_secs)

        self.minutes.set(str(self.max_mins))
        self.hours.set(str(self.max_hour))
        self.seconds.set(str(self.max_secs))

        self.pause_minutes = StringVar()
        self.pause_hours = StringVar()
        self.pause_seconds = StringVar()

        self.pause_max_mins, self.pause_max_secs = divmod(
            self.max_pause, 60)
        self.pause_max_hour, self.pause_mins = divmod(self.pause_max_mins, 60)

        if self.pause_max_mins < 10:
            self.pause_max_mins = "0" + str(self.pause_max_mins)
        if self.pause_max_hour < 10:
            self.pause_max_hour = "0" + str(self.pause_max_hour)
        if self.pause_max_secs < 10:
            self.pause_max_secs = "0" + str(self.pause_max_secs)

        self.pause_minutes.set(str(self.pause_max_mins))
        self.pause_hours.set(str(self.pause_max_hour))
        self.pause_seconds.set(str(self.pause_max_secs))

    def sound(self):
        mixer.music.load(r'Timer/end.wav')
        mixer.music.play(loops=3)


root = Tk()
app = App(root)
root.mainloop()
