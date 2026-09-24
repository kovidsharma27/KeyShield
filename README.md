# KeyShield

A Python-based endpoint telemetry and detection demonstration for cybersecurity education.

## Overview

KeyShield demonstrates a simplified blue-team workflow:

**Endpoint Telemetry → Event Analysis → Detection → Reporting**

The application provides a controlled environment for recording keyboard event types from its own text box and analyzing the resulting session activity.

## Features

- Controlled keyboard-event monitoring
- Start/Stop session controls
- Privacy-preserving telemetry
- CSV session logging
- Automatic session numbering
- Event statistics
- Event-rate analysis
- Rule-based activity detection
- Session report generation
- Simple Tkinter graphical interface

## Demo

![KeyShield Demo](screenshots/keyshield-demo.png)

## Telemetry

KeyShield records event types rather than the actual characters typed.

Recorded event types include:

- `CHARACTER`
- `SPACE`
- `ENTER`
- `BACKSPACE`

Example telemetry:

    timestamp,event_type
    2026-09-24 21:10:12,CHARACTER
    2026-09-24 21:10:12,CHARACTER
    2026-09-24 21:10:13,SPACE
    2026-09-24 21:10:14,ENTER

## Detection

After a session ends, KeyShield calculates:

- Total events
- Session duration
- Events per second
- Event-type breakdown

A simple threshold-based rule flags unusually high event rates.

**Detection rule:** Event rate greater than 8 events per second → `HIGH EVENT RATE`

Otherwise → `NORMAL`

This is intentionally a simple rule-based detector rather than a machine-learning model.

## Project Structure

    KeyShield/
    ├── screenshots/
    │   └── keyshield-demo.png
    ├── sessions/
    │   └── .gitkeep
    ├── src/
    │   └── main.py
    ├── .gitignore
    ├── README.md
    └── requirements.txt

## Installation

Clone the repository and enter the project directory.

`git clone https://github.com/kovidsharma27/KeyShield.git`

`cd KeyShield`

Create a virtual environment.

`python -m venv .virtual`

Activate it on Windows PowerShell.

`.\.virtual\Scripts\Activate.ps1`

Install dependencies.

`pip install -r requirements.txt`

Run KeyShield.

`python src/main.py`

## Usage

1. Launch KeyShield.
2. Click **START SESSION**.
3. Type test text into the application text box.
4. Click **STOP SESSION**.
5. Review the generated session report.
6. Session telemetry is saved as a CSV file in `sessions/`.

## Privacy and Safety

KeyShield is designed for authorized cybersecurity demonstrations.

It does not:

- capture passwords
- monitor other applications
- record actual typed characters in telemetry
- transmit collected data
- use stealth mechanisms
- use persistence mechanisms

Only use the application with input you are authorized to monitor.

## Technologies

- Python
- Tkinter
- CSV
- Git
- GitHub

## Future Improvements

Possible future improvements include:

- Improved telemetry visualization
- Additional endpoint telemetry
- More advanced detection rules
- Anomaly detection
- Machine-learning-based analysis

## Author

**Kovid Sharma**

Cybersecurity project focused on endpoint telemetry, detection, and defensive security concepts.