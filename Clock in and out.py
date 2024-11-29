import time
import tkinter as tk

def start_work():
    return time.time()

def stop_work():
    return time.time()

def calculate_work_time(start_time, stop_time):
    elapsed_time = stop_time - start_time
    hours_float, remainder = divmod(elapsed_time, 3600)
    minutes_float, _ = divmod(remainder, 60)
    hours = int(hours_float)
    minutes = int(minutes_float)
    return hours, minutes

def start_working():
    global start_time
    start_time = start_work()
    start_button["state"] = "disabled"
    stop_button["state"] = "normal"

def stop_working():
    global start_time
    stop_time = stop_work()
    hours_worked, minutes_worked = calculate_work_time(start_time, stop_time)
    result_label.config(text=f"Worked: {hours_worked} hours and {minutes_worked} minutes")
    start_button["state"] = "normal"
    stop_button["state"] = "disabled"

root = tk.Tk()
root.title("Punch In/Out Clock")
root.geometry("300x200")

frame = tk.Frame(root)
frame.pack(pady=20)

start_button = tk.Button(frame, text="Start Working", command=start_working, width=20)
stop_button = tk.Button(frame, text="Stop Working", command=stop_working, state="disabled", width=20)
result_label = tk.Label(root, text="", font=("Helvetica", 16))

start_button.pack(pady=10)
stop_button.pack(pady=10)
result_label.pack()

root.mainloop()