<div align="center">

Hand Mouse Control

Control your Windows mouse with real-time hand gestures and a webcam.






Download EXE · View Source · Report an Issue

</div>

What is this?

Hand Mouse Control is a Windows application that turns a webcam into a hands-free mouse interface.

It tracks your hands in real time, interprets a small set of gestures, and translates them into normal Windows mouse actions such as moving, clicking, dragging, and scrolling.

The project is built with Python and uses MediaPipe Hand Landmarker for hand tracking, OpenCV for camera processing, PyAutoGUI for mouse control, NumPy for coordinate calculations, and Tkinter for the settings interface.

No special hardware is required beyond a compatible webcam.

Features

<table>
<tr>
<td width="50%">

Mouse Control

Move the cursor with your right hand

Click-and-drag with a pinch gesture

Scroll vertically with a dedicated gesture

Smooth cursor movement with configurable smoothing

</td>
<td width="50%">

Gesture Input

Two-hand interaction

Left and right click gestures

Gesture latching to prevent repeated clicks

Configurable pinch and finger detection sensitivity

</td>
</tr>
<tr>
<td width="50%">

Camera & Tracking

Real-time webcam tracking

Up to two detected hands

Camera switching

Live FPS and camera status

Hand landmark visualization

</td>
<td width="50%">

Configuration

Pause/resume mouse control

Swap left/right hand roles

Tracking-area adjustment

Scroll speed adjustment

Finger-up sensitivity

Separate Settings window

</td>
</tr>
</table>

Gesture Guide

Right hand — movement and actions

Gesture

Action

Move index finger

Move the cursor

Thumb + index pinch

Hold the mouse button for drag-and-drop

Thumb + ring-finger pinch

Enter scroll mode

Left hand — clicking

Gesture

Action

Index finger raised

Right click

Index + middle fingers raised

Left click

Clicks are triggered on the start of the gesture, rather than once every frame. This prevents a held gesture from producing a stream of clicks.

Controls at a glance

Key

Action

P

Pause / resume mouse control

S

Show / hide the overlay panel

C

Switch to the next camera

Q

Quit

ESC

Quit

Keyboard shortcuts are handled while the camera window is focused.

How it works

The application is built around a simple real-time pipeline:

┌──────────────┐
│    Webcam    │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│ Camera Capture      │
│ Background Thread   │
└─────────┬───────────┘
          │ newest frame
          ▼
┌─────────────────────┐
│ MediaPipe Hand      │
│ Landmarker          │
└─────────┬───────────┘
          │ 21 landmarks / hand
          ▼
┌─────────────────────┐
│ Gesture Processing  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ PyAutoGUI           │
│ Mouse Actions       │
└─────────────────────┘

Camera capture

The webcam is read on a dedicated background thread. The processing loop works with the newest available frame instead of waiting for a blocking camera read every iteration.

This is designed to reduce the amount of stale camera data waiting in a queue and helps keep the interaction responsive.

Hand tracking

MediaPipe Hand Landmarker detects the user's hands and provides the landmark coordinates used by the application.

The program supports two detected hands and maps them to the left-hand and right-hand interaction roles.

Gesture detection

The gesture system checks landmark positions and distances to determine whether the user is moving, pinching, scrolling, or performing a click gesture.

Cursor mapping

Hand coordinates are normalized to the camera frame and mapped into the available screen area. A configurable smoothing value is applied before the mouse pointer is moved.

Lost-hand cleanup

When tracking is temporarily lost, active mouse states are cleaned up. For example, a drag is released rather than leaving the mouse button held down.

Settings

The application opens a separate Settings window with live controls.

Setting

Purpose

Pause mouse control

Temporarily stop mouse actions while keeping tracking active

Swap left/right hand

Reverse which detected hand is assigned to each role

Smoothing

Reduce cursor jitter or make movement more responsive

Pinch sensitivity

Adjust the distance required for pinch gestures

Scroll speed

Change the amount of scrolling produced by hand movement

Tracking area size

Change how much of the camera frame is mapped to the screen

Finger-up sensitivity

Adjust how raised fingers are detected

Camera index

Select a camera when multiple cameras are connected

Getting started

There are two ways to use the project:

Method

Best for

Pre-built EXE

Running the application without installing Python

Run from source

Development, testing, debugging, and modification

Option A — Run the pre-built EXE

The standalone Windows executable is published separately under GitHub Releases.

Download

Download the latest Windows release

Download HandMouseControl.exe and run it on a supported Windows system.

The EXE is separate from the source tree so the repository stays focused on the actual project files.

Option B — Run from source

Running from source does not require the compiled EXE.

Requirements

Windows 10 or Windows 11

Python compatible with the installed MediaPipe version

A working webcam

Internet access for installing Python packages

Python 3.10–3.12 is the practical target for this project.

1. Clone the repository

git clone https://github.com/Vergil-pain/HandMouseControl.git
cd HandMouseControl

2. Check Python

python --version

3. Install dependencies

python -m pip install -r requirements.txt

4. Start the application

python main.py

The program opens the camera/tracking window and the Settings window.

Camera permissions

If the camera does not work, check:

Windows Settings → Privacy & security → Camera

Make sure camera access is enabled for desktop applications.

If more than one camera is connected, use the Camera index setting or press C in the camera window to switch cameras.

Build your own EXE

The repository includes build.bat for creating the standalone executable with PyInstaller.

Build

Run:

build.bat

The compiled application is produced under:

dist\HandMouseControl.exe

The build configuration is intended to bundle the application into a Windows executable so Python does not need to be installed on the target machine.

If the EXE behaves differently from the source version, run python main.py from a Command Prompt first. That makes Python errors visible and is the easiest way to separate a Python/runtime problem from a packaging problem.

Project structure

HandMouseControl/
├── main.py
├── build.bat
├── requirements.txt
├── hand_landmarker.task
├── icon.ico
└── README.md

File

Purpose

main.py

Main application, camera processing, gesture detection, mouse control, and settings UI

build.bat

Build script for the Windows executable

requirements.txt

Python package requirements

hand_landmarker.task

MediaPipe hand-tracking model

icon.ico

Windows application icon

README.md

Project documentation

MediaPipe model

hand_landmarker.task is the hand-tracking model used by MediaPipe Hand Landmarker.

The model provides the landmark data the application uses to recognize hand position and gestures.

Keeping the model file with the project also makes source-based setup and packaging easier to understand and reproduce.

Architecture

The application separates camera capture from frame processing:

Camera thread → captures frames continuously and keeps the newest frame available.

Tracking / processing loop → receives the latest frame, runs MediaPipe, detects gestures, updates the UI overlay, and sends mouse actions through PyAutoGUI.

Settings window → provides live configuration controls through Tkinter.

This separation is intended to avoid making the mouse-control loop wait unnecessarily on webcam capture.

Troubleshooting

<details>
<summary><strong>The application does not start</strong></summary>

Run it from Command Prompt:

python main.py

This exposes the actual Python error instead of hiding it behind a double-click.

</details>

<details>
<summary><strong>The camera window is black or says there is no signal</strong></summary>

Check Windows camera permissions and make sure another application is not already using the webcam.

Try another camera index from the Settings window or press C while the camera window is focused.

</details>

<details>
<summary><strong>The cursor is too jittery</strong></summary>

Increase Smoothing in the Settings window.

</details>

<details>
<summary><strong>The cursor feels delayed</strong></summary>

Lower the Smoothing value and make sure another application is not heavily using the webcam.

</details>

<details>
<summary><strong>Pinch gestures trigger too easily or not easily enough</strong></summary>

Adjust Pinch sensitivity in the Settings window.

</details>

<details>
<summary><strong>Click gestures trigger incorrectly</strong></summary>

Adjust Finger-up sensitivity and make sure the intended gesture is clearly visible to the camera.

</details>

<details>
<summary><strong>Left and right hands seem reversed</strong></summary>

Enable Swap left/right hand in the Settings window.

</details>

<details>
<summary><strong>MediaPipe cannot load the model</strong></summary>

Make sure hand_landmarker.task exists in the project directory when running from source.

If you are building the application yourself, rebuild the executable after changing the project files.

</details>

<details>
<summary><strong>The EXE does not start</strong></summary>

Try the source version first:

python main.py

If the source version works but the EXE does not, rebuild with:

build.bat

Running the source version from a terminal is also useful for finding missing dependencies or runtime errors.

</details>

Privacy

The application uses the webcam for real-time hand tracking and mouse control.

The project does not intentionally upload webcam frames or hand-tracking data to an online service as part of its normal mouse-control workflow.

Internet access may still be needed for installing Python packages or obtaining project dependencies when setting up from source.

Security

Only run the source code or executable from a copy of the project you trust.

Packaged Python applications can sometimes trigger antivirus or security software because of how bundled executables are structured. Review any warning before allowing an executable to run.

Development

The repository is intended to be usable both as an application and as a development project.

Typical development flow:

python -m pip install -r requirements.txt
python main.py

After making changes, rebuild the Windows application with:

build.bat

Contributing

Contributions, bug reports, and suggestions are welcome.

For a code contribution:

Fork the repository.

Make your changes.

Test the changed behavior.

Open a pull request with a clear description.

When reporting a bug, include useful details such as:

Windows version

Python version, if running from source

Camera information

Error message or console output

Steps to reproduce the problem

Release

The project keeps the source code and the compiled application separate:

Repository: source code, model, build script, dependencies, and documentation

GitHub Releases: compiled Windows executable

Current release

v1.0.0

Download HandMouseControl v1.0.0

Contact

Have a bug report, suggestion, or question?

Telegram: @XRO_G

Author

XRO

Telegram: @XRO_G

License

No specific open-source license is currently included with this project.

<div align="center">

Hand Mouse Control

Made with Python · OpenCV · MediaPipe · PyAutoGUI

</div>
