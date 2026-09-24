import tkinter as tk
from datetime import datetime
from pathlib import Path
import csv
from tkinter import messagebox

# Session data
session_active = False
event_count = 0
character_count = 0
space_count = 0
enter_count = 0
backspace_count = 0
session_start = None

session_events = []
session_number = 1

def start_session():
    global session_active
    global event_count
    global character_count
    global space_count
    global enter_count
    global backspace_count
    global session_start
    global session_events

    session_active = True

    event_count = 0
    character_count = 0
    space_count = 0
    enter_count = 0
    backspace_count = 0

    session_events = []

    session_start = datetime.now()

    status_label.config(text="Status: RECORDING")
    detection_label.config(text="Detection: Monitoring active")

    start_button.config(state="disabled")
    stop_button.config(state="normal")

    update_statistics()

    text_box.delete("1.0", tk.END)
    text_box.focus()

def stop_session():
    global session_active

    if not session_active:
        return

    session_active = False

    save_session()
    generate_report()

    status_label.config(text="Status: STOPPED")
    detection_label.config(text="Detection: Analysis complete")

    start_button.config(state="normal")
    stop_button.config(state="disabled")

def generate_report():
    if not session_events:
        messagebox.showinfo(
            "KeyShield Report",
            "No events were recorded in this session."
        )
        return

    first_time = datetime.strptime(
        session_events[0][0], "%Y-%m-%d %H:%M:%S"
    )

    last_time = datetime.strptime(
        session_events[-1][0], "%Y-%m-%d %H:%M:%S"
    )

    duration = (last_time - first_time).total_seconds()

    if duration == 0:
        events_per_second = len(session_events)
    else:
        events_per_second = len(session_events) / duration

    character_total = sum(
        1 for _, event in session_events if event == "CHARACTER"
    )

    space_total = sum(
        1 for _, event in session_events if event == "SPACE"
    )

    enter_total = sum(
        1 for _, event in session_events if event == "ENTER"
    )

    backspace_total = sum(
        1 for _, event in session_events if event == "BACKSPACE"
    )

    if events_per_second > 8:
        activity_flag = "HIGH EVENT RATE"
    else:
        activity_flag = "NORMAL"

    report = (
        "===== KeyShield Session Report =====\n\n"
        f"Total events: {len(session_events)}\n"
        f"Duration: {duration:.2f} seconds\n"
        f"Event rate: {events_per_second:.2f} events/sec\n\n"
        "Event breakdown:\n"
        f"CHARACTER: {character_total}\n"
        f"SPACE: {space_total}\n"
        f"ENTER: {enter_total}\n"
        f"BACKSPACE: {backspace_total}\n\n"
        f"Activity flag: {activity_flag}"
    )

    print("\n" + report)

    messagebox.showinfo(
        "KeyShield Session Report",
        report
    )

def save_session():
    sessions_folder = Path("sessions")
    sessions_folder.mkdir(exist_ok=True)

    session_number = get_next_session_number()

    filename = sessions_folder / f"session_{session_number:03d}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["timestamp", "event_type"])

        for timestamp, event_type in session_events:
            writer.writerow([timestamp, event_type])

    print(f"Session saved to: {filename}")

def record_key(event):
    global event_count
    global character_count
    global space_count
    global enter_count
    global backspace_count

    if not session_active:
        return

    event_count += 1

    event_type = None

    if event.keysym == "space":
        space_count += 1
        event_type = "SPACE"

    elif event.keysym == "Return":
        enter_count += 1
        event_type = "ENTER"

    elif event.keysym == "BackSpace":
        backspace_count += 1
        event_type = "BACKSPACE"

    elif len(event.char) == 1:
        character_count += 1
        event_type = "CHARACTER"

    if event_type:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_events.append((timestamp, event_type))

    update_statistics()

def update_statistics():
    event_label.config(text=f"Total events: {event_count}")
    character_label.config(text=f"Characters: {character_count}")
    space_label.config(text=f"Spaces: {space_count}")
    enter_label.config(text=f"Enter: {enter_count}")
    backspace_label.config(text=f"Backspace: {backspace_count}")


def close_app():
    root.destroy()

def get_next_session_number():
    sessions_folder = Path("sessions")
    sessions_folder.mkdir(exist_ok=True)

    existing_files = list(sessions_folder.glob("session_*.csv"))

    if not existing_files:
        return 1

    numbers = []

    for file in existing_files:
        try:
            number = int(file.stem.split("_")[1])
            numbers.append(number)
        except (IndexError, ValueError):
            continue

    if not numbers:
        return 1

    return max(numbers) + 1

# Application window

root = tk.Tk()

root.title("KeyShield")
root.geometry("700x600")
root.resizable(False, False)

# Title
title_label = tk.Label(
    root,
    text="KeyShield",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=(20, 5))

subtitle_label = tk.Label(
    root,
    text="Endpoint Telemetry Demonstration",
    font=("Arial", 11)
)

subtitle_label.pack()

# Status
status_label = tk.Label(
    root,
    text="Status: STOPPED",
    font=("Arial", 12, "bold")
)

status_label.pack(pady=15)

# Input area
instruction_label = tk.Label(
    root,
    text="Type your test text below:"
)

instruction_label.pack()

text_box = tk.Text(
    root,
    height=8,
    width=65
)
text_box.pack(pady=10)

# Capture events only from our text box
text_box.bind("<KeyPress>", record_key)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="START SESSION",
    command=start_session,
    width=15
)

start_button.pack(side="left", padx=5)

stop_button = tk.Button(
    button_frame,
    text="STOP SESSION",
    command=stop_session,
    width=15,
    state="disabled"
)

stop_button.pack(side="left", padx=5)

# Statistics
stats_frame = tk.Frame(root)
stats_frame.pack(pady=15)

event_label = tk.Label(stats_frame, text="Total events: 0")
event_label.pack()

character_label = tk.Label(stats_frame, text="Characters: 0")
character_label.pack()

space_label = tk.Label(stats_frame, text="Spaces: 0")
space_label.pack()

enter_label = tk.Label(stats_frame, text="Enter: 0")
enter_label.pack()

backspace_label = tk.Label(stats_frame, text="Backspace: 0")
backspace_label.pack()

detection_label = tk.Label(
    root,
    text="Detection: Monitoring inactive",
    font=("Arial", 11, "bold")
)

detection_label.pack(pady=5)

# Exit
close_button = tk.Button(
    root,
    text="EXIT",
    command=close_app,
    width=10
)

close_button.pack(pady=10)

root.mainloop()