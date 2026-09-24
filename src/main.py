import csv
import tkinter as tk
from datetime import datetime, timezone
from pathlib import Path
from tkinter import messagebox

# Session state
session_active = False

event_count = 0
character_count = 0
space_count = 0
enter_count = 0
backspace_count = 0

session_start = None
session_end = None

session_events = []

def start_session():
    """Start a new telemetry session."""

    global session_active
    global event_count
    global character_count
    global space_count
    global enter_count
    global backspace_count
    global session_start
    global session_end
    global session_events

    session_active = True

    # Reset statistics
    event_count = 0
    character_count = 0
    space_count = 0
    enter_count = 0
    backspace_count = 0

    # Reset session timestamps
    session_start = datetime.now(timezone.utc)
    session_end = None

    # Clear previous session telemetry
    session_events = []

    # Update interface
    status_label.config(text="Status: RECORDING")
    detection_label.config(text="Detection: Monitoring active")

    start_button.config(state="disabled")
    stop_button.config(state="normal")

    update_statistics()

    # Clear the controlled input box
    text_box.delete("1.0", tk.END)
    text_box.focus()

def stop_session():
    """Stop the current telemetry session."""

    global session_active
    global session_end

    if not session_active:
        return

    # Record the actual session end time
    session_end = datetime.now(timezone.utc)

    session_active = False

    # Update interface before displaying the report
    status_label.config(text="Status: STOPPED")
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    detection_label.config(text="Detection: Analysis complete")

    # Save telemetry and generate report
    save_session()
    generate_report()

def record_key(event):
    """
    Record a keyboard event from the controlled text box.

    Only event types are stored:
    CHARACTER, SPACE, ENTER, BACKSPACE

    Actual typed characters are never stored.
    """

    global event_count
    global character_count
    global space_count
    global enter_count
    global backspace_count

    if not session_active:
        return

    event_type = None

    # Space
    if event.keysym == "space":
        space_count += 1
        event_type = "SPACE"

    # Enter
    elif event.keysym == "Return":
        enter_count += 1
        event_type = "ENTER"

    # Backspace
    elif event.keysym == "BackSpace":
        backspace_count += 1
        event_type = "BACKSPACE"

    # Character
    elif len(event.char) == 1:
        character_count += 1
        event_type = "CHARACTER"

    # Store only valid telemetry events
    if event_type:
        event_count += 1

        # Timestamp includes milliseconds for better telemetry precision
        timestamp = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]

        session_events.append(
            (timestamp, event_type)
        )

    update_statistics()

def update_statistics():
    """Update statistics displayed in the GUI."""

    event_label.config(
        text=f"Total events: {event_count}"
    )

    character_label.config(
        text=f"Characters: {character_count}"
    )

    space_label.config(
        text=f"Spaces: {space_count}"
    )

    enter_label.config(
        text=f"Enter: {enter_count}"
    )

    backspace_label.config(
        text=f"Backspace: {backspace_count}"
    )

def get_next_session_number():
    """Find the next available session number."""

    sessions_folder = Path("sessions")
    sessions_folder.mkdir(exist_ok=True)

    existing_files = list(
        sessions_folder.glob("session_*.csv")
    )

    if not existing_files:
        return 1

    numbers = []

    for file in existing_files:
        try:
            number = int(
                file.stem.split("_")[1]
            )

            numbers.append(number)

        except (IndexError, ValueError):
            continue

    if not numbers:
        return 1

    return max(numbers) + 1

def save_session():
    """Save privacy-preserving telemetry to a CSV file."""

    sessions_folder = Path("sessions")
    sessions_folder.mkdir(exist_ok=True)

    session_number = get_next_session_number()

    filename = (
        sessions_folder /
        f"session_{session_number:03d}.csv"
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["timestamp", "event_type"]
        )

        for timestamp, event_type in session_events:

            writer.writerow(
                [timestamp, event_type]
            )

    print(
        f"Session saved to: {filename}"
    )

def generate_report():
    """Generate and display the session analysis report."""

    if not session_events:

        messagebox.showinfo(
            "KeyShield Report",
            "No events were recorded in this session."
        )

        return

    if session_start is not None and session_end is not None:

        duration = (
            session_end - session_start
        ).total_seconds()

    else:

        duration = 0

    # Prevent division by zero
    if duration <= 0:

        events_per_second = len(session_events)

    else:

        events_per_second = (
            len(session_events) / duration
        )

    character_total = sum(
        1
        for _, event in session_events
        if event == "CHARACTER"
    )

    space_total = sum(
        1
        for _, event in session_events
        if event == "SPACE"
    )

    enter_total = sum(
        1
        for _, event in session_events
        if event == "ENTER"
    )

    backspace_total = sum(
        1
        for _, event in session_events
        if event == "BACKSPACE"
    )

    if events_per_second > 8:

        activity_flag = "HIGH EVENT RATE"

    else:

        activity_flag = "NORMAL"

    report = (
        "===== KeyShield Session Report =====\n\n"

        f"Total events: {len(session_events)}\n"

        f"Duration: {duration:.2f} seconds\n"

        f"Event rate: "
        f"{events_per_second:.2f} events/sec\n\n"

        "Event breakdown:\n"

        f"CHARACTER: {character_total}\n"

        f"SPACE: {space_total}\n"

        f"ENTER: {enter_total}\n"

        f"BACKSPACE: {backspace_total}\n\n"

        f"Activity flag: {activity_flag}"
    )

    # Print report to terminal
    print("\n" + report)

    # Display report in GUI
    messagebox.showinfo(
        "KeyShield Session Report",
        report
    )

def close_app():
    """Close the KeyShield application."""

    root.destroy()

root = tk.Tk()

root.title("KeyShield")

root.geometry("700x600")

root.resizable(False, False)

title_label = tk.Label(
    root,
    text="KeyShield",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=(20, 5)
)


subtitle_label = tk.Label(
    root,
    text="Endpoint Telemetry Demonstration",
    font=("Arial", 11)
)

subtitle_label.pack()

status_label = tk.Label(
    root,
    text="Status: STOPPED",
    font=("Arial", 12, "bold")
)

status_label.pack(
    pady=15
)

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

text_box.pack(
    pady=10
)


# Capture keyboard events ONLY from this text box
text_box.bind(
    "<KeyPress>",
    record_key
)

button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)


start_button = tk.Button(
    button_frame,
    text="START SESSION",
    command=start_session,
    width=15
)

start_button.pack(
    side="left",
    padx=5
)


stop_button = tk.Button(
    button_frame,
    text="STOP SESSION",
    command=stop_session,
    width=15,
    state="disabled"
)

stop_button.pack(
    side="left",
    padx=5
)


stats_frame = tk.Frame(root)

stats_frame.pack(
    pady=15
)


event_label = tk.Label(
    stats_frame,
    text="Total events: 0"
)

event_label.pack()


character_label = tk.Label(
    stats_frame,
    text="Characters: 0"
)

character_label.pack()


space_label = tk.Label(
    stats_frame,
    text="Spaces: 0"
)

space_label.pack()


enter_label = tk.Label(
    stats_frame,
    text="Enter: 0"
)

enter_label.pack()


backspace_label = tk.Label(
    stats_frame,
    text="Backspace: 0"
)

backspace_label.pack()

detection_label = tk.Label(
    root,
    text="Detection: Monitoring inactive",
    font=("Arial", 11, "bold")
)

detection_label.pack(
    pady=5
)


close_button = tk.Button(
    root,
    text="EXIT",
    command=close_app,
    width=10
)

close_button.pack(
    pady=10
)

root.mainloop()