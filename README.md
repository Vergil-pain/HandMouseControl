<div align="center">

🖐️ Hand Mouse Control

Control your Windows mouse with real-time hand gestures and a webcam.







English · فارسی

</div>

🌟 What is Hand Mouse Control?

Hand Mouse Control is a Windows application that lets you control the mouse with your hands through a webcam.

The idea is simple: the webcam captures your hand, MediaPipe tracks the hand landmarks in real time, and the application converts those movements into normal Windows mouse actions.

The project is designed around two-hand interaction:

Hand

Main role

🖐️ Right hand

Cursor movement, drag and drop, scrolling

🤚 Left hand

Left click and right click

The application also includes a separate Settings window, live status information, camera switching, gesture overlays, and keyboard shortcuts.

💡 You can run the program directly from Python, or use the pre-built Windows .exe from the GitHub Releases page.

✨ Features

🖱️ Mouse control

Move the cursor with the right index finger.

Hold the mouse button for drag-and-drop using a thumb + index pinch.

Enter scrolling mode using a thumb + ring-finger pinch.

Automatically release the mouse button if the tracked hand disappears during a drag.

🤏 Gesture controls

One raised finger on the left hand → right click.

Two raised fingers on the left hand → left click.

Click gestures are latched so holding a gesture does not trigger a new click every frame.

⚙️ Live settings

Change the following values while the program is running:

Cursor smoothing

Pinch sensitivity

Scroll speed

Tracking area size

Finger-up sensitivity

Camera index

Left/right hand swapping

Mouse pause state

🎥 Camera and interface

Background camera capture thread.

Live hand landmark visualization.

FPS display.

Camera status display.

On-screen gesture information.

Camera switching.

Separate Settings window.

🎮 Gesture Guide

Right hand

Gesture

Action

Description

☝️ Move index finger

Move cursor

Your index fingertip is mapped to the screen.

🤏 Thumb + index pinch

Drag

Holds the mouse button while the fingers stay pinched.

🤏 Thumb + ring pinch

Scroll

Vertical hand movement controls scrolling.

Left hand

Gesture

Action

Description

☝️ Index finger only

Right click

A single raised finger triggers one right-click.

✌️ Index + middle fingers

Left click

Two raised fingers trigger one left-click.

🔄 Hand orientation: The camera preview is mirrored. The application adjusts MediaPipe's hand labels to match the physical hand shown in the preview. If your setup still feels reversed, enable Swap left/right hand in Settings.

🪟 The two application windows

When the program starts, it opens two windows.

🎥 Camera window

The camera window shows:

The live webcam image.

Detected hand landmarks.

Current tracking state.

FPS.

Right-hand gesture status.

Left-hand click status.

A small help/legend panel.

The camera window also receives the keyboard shortcuts listed below.

⚙️ Settings window

The Settings window provides live controls for:

Setting

What it changes

Pause mouse control

Temporarily stops mouse actions.

Swap left/right hand

Swaps the logical roles of the detected hands.

Smoothing

Higher values make movement smoother but can add more latency.

Pinch sensitivity

Changes how close two fingertips must be to count as a pinch.

Scroll speed

Changes the amount of scrolling produced by hand movement.

Tracking area size

Controls how much of the camera frame is mapped to the full screen.

Finger-up sensitivity

Changes how far a fingertip must be raised to count as an up finger.

Camera index

Selects which connected camera is used.

Changes are applied while the program is running.

⌨️ Keyboard shortcuts

The shortcuts below work while the camera window is focused.

Key

Action

P

Pause / resume mouse control

S

Show / hide the legend panel

C

Switch to the next camera

Q

Quit

ESC

Quit

🧠 How it works

The application follows a simple real-time pipeline:

Webcam
   │
   ▼
Camera Capture Thread
   │
   ▼
Newest Available Frame
   │
   ▼
MediaPipe Hand Landmarker
   │
   ▼
Hand + Landmark Detection
   │
   ▼
Gesture Processing
   │
   ├── Cursor movement
   ├── Drag
   ├── Scroll
   ├── Left click
   └── Right click
   │
   ▼
Windows Mouse

1. Camera capture

The webcam is read on a dedicated background thread.

Instead of making the processing loop wait for every camera read, the camera thread continuously updates the newest frame available. This helps prevent old frames from building up in the queue and reduces the feeling of delayed input.

The program requests a camera frame size of approximately 640×480 and attempts to use a small capture buffer where the backend supports it.

2. Hand tracking

MediaPipe Hand Landmarker processes the newest RGB camera frame.

The application runs the tracker in VIDEO mode and allows detection of up to two hands.

For each detected hand, MediaPipe provides the hand landmarks used by the gesture logic.

3. Hand classification

The camera preview is mirrored so it feels natural to the user.

Because mirroring changes the visual left/right relationship, the program adjusts the MediaPipe handedness label and also provides a manual Swap left/right hand option.

4. Cursor mapping

The right index fingertip is represented by normalized coordinates inside the camera frame.

The active tracking area is converted into screen coordinates, then the result is passed through the smoothing system before PyAutoGUI moves the real Windows cursor.

5. Gesture detection

The application uses landmark distances and finger positions to detect the supported gestures.

Examples:

Thumb-to-index distance → drag gesture.

Thumb-to-ring distance → scroll gesture.

Index/middle finger positions → left/right click gestures.

6. Mouse state cleanup

The program keeps track of whether dragging or scrolling is active.

If the right hand disappears while dragging, the application releases the mouse button and clears the scroll state so the system does not remain in a stuck input state.

7. Settings and runtime state

The Tkinter Settings window updates the shared configuration while the camera-processing logic continues to run.

The interface also displays the current FPS and camera status.

🛠️ Technology stack

Technology

Purpose

🐍 Python

Main application logic

🎥 OpenCV

Webcam capture and image processing

✋ MediaPipe Hand Landmarker

Real-time hand and landmark detection

🖱️ PyAutoGUI

Windows mouse control

🔢 NumPy

Coordinate mapping and numerical operations

🪟 Tkinter

Settings window and controls

📦 PyInstaller

Standalone Windows executable

📦 MediaPipe model

The repository includes:

hand_landmarker.task

This is the MediaPipe hand-tracking model used by the application.

When the program starts, it checks for the model in the application directory. When the file is not available, the program can download the model from the configured MediaPipe model URL.

For a source checkout, keeping hand_landmarker.task next to main.py is recommended.

When the program is built with the provided build.bat, the build command adds the model file to the packaged application data and also collects MediaPipe's required package data.

🚀 Run from source

You do not need the .exe to develop or run the project from source.

Requirements

Windows 10 or Windows 11

Python

A working webcam

Camera access enabled in Windows

The packages listed in requirements.txt

For this project's MediaPipe dependency, Python 3.10–3.12 is a practical starting range. Exact compatibility can still depend on the package versions available when you install them.

1. Check Python

python --version

2. Install dependencies

python -m pip install -r requirements.txt

3. Start the application

python main.py

On startup, the program should open:

The camera/tracking window.

The Settings window.

🏗️ Build the standalone EXE

The project includes:

build.bat

You can double-click it or run it from a Command Prompt:

build.bat

The script:

Installs the Python requirements.

Installs PyInstaller.

Removes old build, dist, and .spec files when present.

Builds a PyInstaller one-file executable.

Applies the application icon.

Adds hand_landmarker.task.

Collects the MediaPipe package data.

Includes the Tkinter modules used by the Settings window.

The final file is created at:

dist\HandMouseControl.exe

📥 Using the EXE

The compiled executable is intended for Windows users who want to run the application without installing Python separately.

The project keeps the source code and the compiled application separate:

GitHub Repository
├── Source code
├── Model
├── Build script
└── Documentation

GitHub Release
└── HandMouseControl.exe

The current release is available from the repository's Releases page.

📁 Project structure

HandMouseControl/
├── main.py
├── build.bat
├── requirements.txt
├── hand_landmarker.task
├── icon.ico
├── README.md
└── README.fa.md

File

Purpose

main.py

Complete application logic.

build.bat

Automated PyInstaller build script.

requirements.txt

Python package requirements.

hand_landmarker.task

MediaPipe hand model.

icon.ico

Windows application icon.

README.md

English documentation.

README.fa.md

Persian documentation.

🧩 Application architecture

The project is organized around a few major runtime components.

Config

Stores shared runtime settings such as smoothing, pinch threshold, scroll speed, camera index, tracking margin, hand swapping, pause state, FPS, and camera status.

CameraStream

Owns the webcam connection and runs frame acquisition on its own background thread.

HandMouseController

Creates the MediaPipe Hand Landmarker and contains the hand-to-mouse logic.

It is responsible for:

hand classification

coordinate mapping

smoothing

gesture detection

clicking

dragging

scrolling

input-state cleanup

SettingsWindow

Builds the Tkinter interface and synchronizes user settings with the running application.

Camera loop

The camera-processing loop combines:

Capture
  ↓
Flip / RGB conversion
  ↓
MediaPipe detection
  ↓
Gesture handling
  ↓
HUD drawing
  ↓
OpenCV window
  ↓
Keyboard input

Per-frame processing is protected so an individual processing error is logged instead of immediately terminating the whole loop.

🔧 Configuration defaults

The application starts with these main defaults:

Option

Default

Camera index

0

Maximum camera indexes checked

4

Tracking frame margin

0.15

Cursor smoothing

0.35

Pinch threshold

0.045

Scroll speed

800

Finger-up margin

0.02

Hand swapping

Disabled

Mouse control

Active

Overlay panel

Visible

These values can be changed live in the Settings window.

🩹 Troubleshooting

<details>
<summary><strong>❌ The application does not start</strong></summary>

Run the source version from Command Prompt:

python main.py

This lets Python print the actual exception or dependency error instead of hiding it behind a GUI executable.

If the Python version works but the EXE does not, rebuild the EXE using the provided build.bat.

</details>

<details>
<summary><strong>📷 The camera is black or not detected</strong></summary>

Open:

Windows Settings → Privacy & security → Camera

Make sure camera access is enabled.

If more than one camera is connected:

press C in the camera window, or

choose another value in Camera index in Settings.

Also make sure another application is not already occupying the webcam.

</details>

<details>
<summary><strong>🎯 The cursor is too jittery</strong></summary>

Increase Smoothing.

Higher smoothing reduces small movements but can introduce additional delay.

</details>

<details>
<summary><strong>🐢 The cursor feels delayed</strong></summary>

Lower Smoothing.

Also check whether another application is using the webcam or placing extra processing load on the system.

</details>

<details>
<summary><strong>🤏 Pinch gestures are unreliable</strong></summary>

Adjust Pinch sensitivity.

If the pinch triggers too easily, change the value in the opposite direction. If it rarely triggers, increase the sensitivity until the gesture becomes reliable for your camera distance and lighting.

</details>

<details>
<summary><strong>☝️ Click gestures are too sensitive or not sensitive enough</strong></summary>

Adjust Finger-up sensitivity in Settings.

The setting controls how far a fingertip must be above its joint position to count as a raised finger.

</details>

<details>
<summary><strong>🔄 The left and right hands are reversed</strong></summary>

Enable:

Swap left/right hand

in the Settings window.

</details>

<details>
<summary><strong>🧠 MediaPipe cannot import after building</strong></summary>

Rebuild using the provided build.bat.

The build command explicitly collects MediaPipe package data and includes the model file required by the application.

</details>

<details>
<summary><strong>🌐 The hand-tracking model cannot be downloaded</strong></summary>

When hand_landmarker.task is missing, the application can attempt to download it.

Check:

internet connectivity

firewall restrictions

whether the application can access the configured MediaPipe model URL

For source usage, you can also keep the provided hand_landmarker.task in the project directory.

</details>

<details>
<summary><strong>🐍 MediaPipe cannot be installed</strong></summary>

The project's requirements use version ranges rather than a single hard-coded MediaPipe version.

If installation fails, check your Python version first:

python --version

A Python 3.10–3.12 environment is a practical place to start for this project.

</details>

<details>
<summary><strong>⏳ The one-file EXE takes a few seconds to start</strong></summary>

A PyInstaller --onefile application has to unpack its bundled files at startup.

A slower first launch can therefore be normal.

</details>

🔒 Privacy

The application uses the webcam for real-time hand tracking and mouse control.

The project does not intentionally upload camera frames or hand-tracking results to an online service.

The camera processing is part of the local application workflow.

Internet access may still be required for:

installing Python packages

downloading the MediaPipe model if it is not available locally

🛡️ Security

Only run the source code or executable from a trusted copy of the project.

Because the application controls the Windows mouse and accesses the webcam, you should understand and trust the code before running it.

PyInstaller-generated applications can sometimes trigger antivirus or reputation warnings. Such a warning should be reviewed rather than automatically ignored.

The safest option is to build the executable yourself from the published source if you do not want to rely on a pre-built binary.

👨‍💻 Development

The repository contains the files needed to inspect, modify, test, and rebuild the application.

A basic development workflow is:

python --version
python -m pip install -r requirements.txt
python main.py

After making changes:

build.bat

The generated executable will appear at:

dist\HandMouseControl.exe

Development tips

Test camera access before debugging gesture logic.

Keep the camera window focused when testing keyboard shortcuts.

Adjust smoothing and gesture sensitivity for the specific webcam setup.

Test both one-hand and two-hand tracking.

Test what happens when a hand disappears during a drag.

🤝 Contributing

Contributions are welcome.

A simple workflow is:

Fork the repository.

Create your changes.

Run the application from source.

Test the gesture and camera behavior.

Submit a Pull Request.

🐛 Bug reports

When reporting an issue, include as much useful information as possible:

Windows version

Python version

Camera model, if relevant

What gesture was being used

What you expected to happen

What actually happened

The error message, if one appeared

Steps needed to reproduce the issue

📦 Releases

The repository keeps development files and the compiled Windows application separate.

Source repository

Contains:

Python source

requirements

MediaPipe model

build script

icons

English and Persian documentation

GitHub Releases

Contains the ready-to-run Windows executable.

Current release:

Hand Mouse Control v1.0.0

View Releases →

📄 License

No specific open-source license is currently included with this project.

Unless a license is added, the source code should not be assumed to be freely reusable, modified, or redistributed under an open-source license.

📬 Contact

Questions, bug reports, suggestions, or feedback are welcome.

Telegram: @XRO_G

<div align="center">

🖐️ Built with Python, OpenCV, MediaPipe, PyAutoGUI and Tkinter.

⭐ Repository · ⬇️ Releases · 💬 Telegram

English · فارسی

</div>
