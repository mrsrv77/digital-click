import tkinter as tk
from tkinter import messagebox
from time import strftime, sleep
import time
import threading

root = tk.Tk()
root.title("Clock, Stopwatch & Alarm")
root.geometry("500x520")
root.config(bg="black")

# ================= CLOCK =================
def time_display():
    current_time = strftime('%H:%M:%S')  # 24-hour real time
    clock_label.config(text=current_time)
    root.after(1000, time_display)

clock_label = tk.Label(root,
                       font=('calibri', 40, 'bold'),
                       bg='purple',
                       fg='white')
clock_label.pack(pady=20)

# ================= STOPWATCH =================
stopwatch_running = False
start_time = 0
elapsed_time = 0

def start_stopwatch():
    global stopwatch_running, start_time
    if not stopwatch_running:
        stopwatch_running = True
        start_time = time.time() - elapsed_time
        update_stopwatch()

def stop_stopwatch():
    global stopwatch_running
    stopwatch_running = False

def reset_stopwatch():
    global stopwatch_running, elapsed_time
    stopwatch_running = False
    elapsed_time = 0
    stopwatch_label.config(text="00:00:00")

def update_stopwatch():
    global elapsed_time
    if stopwatch_running:
        elapsed_time = time.time() - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        stopwatch_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        root.after(1000, update_stopwatch)

stopwatch_label = tk.Label(root,
                           font=('calibri', 30, 'bold'),
                           text="00:00:00",
                           bg="black",
                           fg="white")
stopwatch_label.pack(pady=20)

button_frame = tk.Frame(root, bg="black")
button_frame.pack()

tk.Button(button_frame, text="Start", command=start_stopwatch).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Stop", command=stop_stopwatch).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Reset", command=reset_stopwatch).grid(row=0, column=2, padx=5)

# ================= ALARM =================
alarm_thread = None

def set_alarm():
    alarm_time = alarm_entry.get().strip()

    # Validate 24-hour format
    try:
        time.strptime(alarm_time, "%H:%M:%S")
    except ValueError:
        messagebox.showerror("Invalid Format",
                             "Enter time like: 19:30:00")
        return

    messagebox.showinfo("Alarm Set",
                        f"Alarm set for {alarm_time}")

    threading.Thread(target=check_alarm,
                     args=(alarm_time,),
                     daemon=True).start()

def check_alarm(alarm_time):
    while True:
        current_time = strftime('%H:%M:%S')

        if current_time == alarm_time:
            root.after(0, lambda:
                       messagebox.showinfo("Alarm",
                                           "⏰ Time to wake up!"))
            break

        sleep(1)

alarm_label = tk.Label(root,
                       text="Set Alarm (HH:MM:SS - 24hr format)",
                       bg="black",
                       fg="white",
                       font=('calibri', 12))
alarm_label.pack(pady=20)

alarm_entry = tk.Entry(root, font=('calibri', 20))
alarm_entry.pack(pady=10)

tk.Button(root, text="Set Alarm", command=set_alarm).pack(pady=5)

# Start real-time clock
time_display()

root.mainloop()
