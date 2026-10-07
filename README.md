<div align="center">

Hand Mouse Control

Choose a language / انتخاب زبان

English   |   فارسی

</div>

<a id="english"></a>

<div align="center">

Hand Mouse Control

Control your Windows mouse with real-time hand gestures and a webcam.







English · فارسی </div>

What is Hand Mouse Control?

Hand Mouse Control is a Windows application that lets you control the mouse with your hands through a webcam.
The idea is simple: the webcam captures your hand, MediaPipe tracks the hand landmarks in real time, and the application converts those movements into normal Windows mouse actions.
The project is designed around two-hand interaction:

Hand

Main role

Right hand

Cursor movement, drag and drop, scrolling

Left hand

Left click and right click

The application also includes a separate Settings window, live status information, camera switching, gesture overlays, and keyboard shortcuts.

You can run the program directly from Python, or use the pre-built Windows .exe from the GitHub Releases page.

Features

Mouse control

Move the cursor with the right index finger.

Hold the mouse button for drag-and-drop using a thumb + index pinch.

Enter scrolling mode using a thumb + ring-finger pinch.

Automatically release the mouse button if the tracked hand disappears during a drag.

Gesture controls

One raised finger on the left hand → right click.

Two raised fingers on the left hand → left click.

Click gestures are latched so holding a gesture does not trigger a new click every frame.

Live settings

Change the following values while the program is running:

Cursor smoothing

Pinch sensitivity

Scroll speed

Tracking area size

Finger-up sensitivity

Camera index

Left/right hand swapping

Mouse pause state

Camera and interface

Background camera capture thread.

Live hand landmark visualization.

FPS display.

Camera status display.

On-screen gesture information.

Camera switching.

Separate Settings window.

Gesture Guide

Right hand

Gesture

Action

Description

Move index finger

Move cursor

Your index fingertip is mapped to the screen.

Thumb + index pinch

Drag

Holds the mouse button while the fingers stay pinched.

Thumb + ring pinch

Scroll

Vertical hand movement controls scrolling.

Left hand

Gesture

Action

Description

Index finger only

Right click

A single raised finger triggers one right-click.

Index + middle fingers

Left click

Two raised fingers trigger one left-click.

Hand orientation: The camera preview is mirrored. The application adjusts MediaPipe's hand labels to match the physical hand shown in the preview. If your setup still feels reversed, enable Swap left/right hand in Settings.

The two application windows

When the program starts, it opens two windows.

Camera window

The camera window shows:

The live webcam image.

Detected hand landmarks.

Current tracking state.

FPS.

Right-hand gesture status.

Left-hand click status.

A small help/legend panel.
The camera window also receives the keyboard shortcuts listed below.

Settings window

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

Keyboard shortcuts

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

How it works

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

Technology stack

Technology

Purpose

Python

Main application logic

OpenCV

Webcam capture and image processing

MediaPipe Hand Landmarker

Real-time hand and landmark detection

PyAutoGUI

Windows mouse control

NumPy

Coordinate mapping and numerical operations

Tkinter

Settings window and controls

PyInstaller

Standalone Windows executable

MediaPipe model

The repository includes:

hand_landmarker.task

This is the MediaPipe hand-tracking model used by the application.
When the program starts, it checks for the model in the application directory. When the file is not available, the program can download the model from the configured MediaPipe model URL.
For a source checkout, keeping hand_landmarker.task next to main.py is recommended.
When the program is built with the provided build.bat, the build command adds the model file to the packaged application data and also collects MediaPipe's required package data.

Run from source

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

Build the standalone EXE

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

Using the EXE

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

Project structure

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

Application architecture

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

Configuration defaults

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

Troubleshooting

<details>
<summary><strong> The application does not start</strong></summary>
Run the source version from Command Prompt:

python main.py

This lets Python print the actual exception or dependency error instead of hiding it behind a GUI executable.
If the Python version works but the EXE does not, rebuild the EXE using the provided build.bat.

</details>

<details>
<summary><strong> The camera is black or not detected</strong></summary>
Open:

Windows Settings → Privacy & security → Camera Make sure camera access is enabled.
If more than one camera is connected:

press C in the camera window, or

choose another value in Camera index in Settings.
Also make sure another application is not already occupying the webcam.

</details>

<details>
<summary><strong> The cursor is too jittery</strong></summary>
Increase **Smoothing**.
Higher smoothing reduces small movements but can introduce additional delay.

</details>

<details>
<summary><strong> The cursor feels delayed</strong></summary>
Lower **Smoothing**.
Also check whether another application is using the webcam or placing extra processing load on the system.

</details>

<details>
<summary><strong> Pinch gestures are unreliable</strong></summary>
Adjust **Pinch sensitivity**.
If the pinch triggers too easily, change the value in the opposite direction. If it rarely triggers, increase the sensitivity until the gesture becomes reliable for your camera distance and lighting.

</details>

<details>
<summary><strong> Click gestures are too sensitive or not sensitive enough</strong></summary>
Adjust **Finger-up sensitivity** in Settings.
The setting controls how far a fingertip must be above its joint position to count as a raised finger.

</details>

<details>
<summary><strong> The left and right hands are reversed</strong></summary>
Enable:

Swap left/right hand

in the Settings window.

</details>

<details>
<summary><strong> MediaPipe cannot import after building</strong></summary>
Rebuild using the provided `build.bat`.
The build command explicitly collects MediaPipe package data and includes the model file required by the application.

</details>

<details>
<summary><strong> The hand-tracking model cannot be downloaded</strong></summary>
When `hand_landmarker.task` is missing, the application can attempt to download it.
Check:

internet connectivity

firewall restrictions

whether the application can access the configured MediaPipe model URL
For source usage, you can also keep the provided hand_landmarker.task in the project directory.

</details>

<details>
<summary><strong> MediaPipe cannot be installed</strong></summary>
The project's requirements use version ranges rather than a single hard-coded MediaPipe version.
If installation fails, check your Python version first:

python --version

A Python 3.10–3.12 environment is a practical place to start for this project.

</details>

<details>
<summary><strong> The one-file EXE takes a few seconds to start</strong></summary>
A PyInstaller `--onefile` application has to unpack its bundled files at startup.
A slower first launch can therefore be normal.

</details>

Privacy

The application uses the webcam for real-time hand tracking and mouse control.
The project does not intentionally upload camera frames or hand-tracking results to an online service.
The camera processing is part of the local application workflow.
Internet access may still be required for:

installing Python packages

downloading the MediaPipe model if it is not available locally

Security

Only run the source code or executable from a trusted copy of the project.
Because the application controls the Windows mouse and accesses the webcam, you should understand and trust the code before running it.
PyInstaller-generated applications can sometimes trigger antivirus or reputation warnings. Such a warning should be reviewed rather than automatically ignored.
The safest option is to build the executable yourself from the published source if you do not want to rely on a pre-built binary.

Development

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

Contributing

Contributions are welcome.
A simple workflow is:

Fork the repository.

Create your changes.

Run the application from source.

Test the gesture and camera behavior.

Submit a Pull Request.

Bug reports

When reporting an issue, include as much useful information as possible:

Windows version

Python version

Camera model, if relevant

What gesture was being used

What you expected to happen

What actually happened

The error message, if one appeared

Steps needed to reproduce the issue

Releases

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

Hand Mouse Control v1.0.0 View Releases →

License

No specific open-source license is currently included with this project.
Unless a license is added, the source code should not be assumed to be freely reusable, modified, or redistributed under an open-source license.

Contact

Questions, bug reports, suggestions, or feedback are welcome.

Telegram: @XRO_G

<div align="center">

Built with Python, OpenCV, MediaPipe, PyAutoGUI and Tkinter.

 Repository ·  Releases ·  Telegram

English · فارسی </div>

<a id="فارسی"></a>

<div align="center">

Hand Mouse Control

کنترل ماوس ویندوز با حرکات دست و وب‌کم، به‌صورت لحظه‌ای







English · فارسی </div>

Hand Mouse Control چیست؟

Hand Mouse Control یک برنامه ویندوزی است که به شما اجازه می‌دهد با استفاده از وب‌کم و حرکات دست، ماوس را کنترل کنید.
ایده ساده است: وب‌کم تصویر دست شما را دریافت می‌کند، MediaPipe نقاط کلیدی دست را به‌صورت لحظه‌ای تشخیص می‌دهد و برنامه این حرکات را به عملیات معمول ماوس ویندوز تبدیل می‌کند.
پروژه بر پایه تعامل هم‌زمان با دو دست طراحی شده است:

دست

وظیفه اصلی

دست راست

حرکت نشانگر، Drag & Drop و اسکرول

دست چپ

Left Click و Right Click

برنامه علاوه بر این‌ها یک پنجره Settings جداگانه، نمایش وضعیت زنده، تعویض دوربین، نمایش اطلاعات ژست‌ها و میانبرهای کیبورد هم دارد.

برای استفاده از نسخه سورس می‌توانید مستقیماً برنامه را با Python اجرا کنید؛ همچنین نسخه آماده .exe از بخش Releases گیت‌هاب در دسترس است.

قابلیت‌ها

کنترل ماوس

حرکت نشانگر با انگشت اشاره دست راست.

نگه‌داشتن دکمه ماوس برای Drag & Drop با Pinch بین شست و انگشت اشاره.

ورود به حالت اسکرول با Pinch بین شست و انگشت حلقه.

آزاد کردن خودکار دکمه ماوس در صورتی که دست هنگام Drag از تصویر خارج شود یا دیگر شناسایی نشود.

کنترل با ژست

یک انگشت بالا در دست چپ → Right Click.

دو انگشت بالا در دست چپ → Left Click.

ژست‌های کلیک به‌صورت Latched پردازش می‌شوند تا نگه داشتن یک ژست باعث اجرای دوباره کلیک در هر فریم نشود.

تنظیمات لحظه‌ای

در هنگام اجرای برنامه می‌توانید موارد زیر را تغییر دهید:

میزان Smooth کردن نشانگر

حساسیت Pinch

سرعت اسکرول

اندازه ناحیه Tracking

حساسیت تشخیص انگشت بالا

شماره دوربین

جابه‌جایی دست چپ و راست

وضعیت Pause کنترل ماوس

دوربین و رابط کاربری

دریافت تصویر دوربین در یک Thread جداگانه.

نمایش زنده نقاط کلیدی دست.

نمایش FPS.

نمایش وضعیت دوربین.

نمایش وضعیت ژست‌ها روی تصویر.

تعویض دوربین.

پنجره Settings جداگانه.

راهنمای ژست‌ها

دست راست

ژست

عملکرد

توضیح

حرکت انگشت اشاره

حرکت نشانگر

نوک انگشت اشاره به مختصات صفحه تبدیل می‌شود.

Pinch شست + اشاره

Drag

تا زمانی که انگشت‌ها نزدیک باشند، دکمه ماوس نگه داشته می‌شود.

Pinch شست + حلقه

Scroll

حرکت عمودی دست برای کنترل اسکرول استفاده می‌شود.

دست چپ

ژست

عملکرد

توضیح

فقط انگشت اشاره

Right Click

یک انگشت بالا یک بار Right Click ایجاد می‌کند.

اشاره + وسط

Left Click

دو انگشت بالا یک بار Left Click ایجاد می‌کنند.

جهت دست‌ها: تصویر دوربین آینه‌ای است تا حرکت طبیعی‌تر به نظر برسد. برنامه برای هماهنگ شدن با تصویر آینه‌ای، برچسب چپ/راست MediaPipe را تنظیم می‌کند. اگر در سیستم شما باز هم نقش دست‌ها برعکس بود، گزینه Swap left/right hand را در Settings فعال کنید.

دو پنجره برنامه

با اجرای برنامه، دو پنجره باز می‌شوند.

پنجره دوربین

پنجره دوربین شامل موارد زیر است:

تصویر زنده وب‌کم.

نقاط کلیدی تشخیص داده‌شده روی دست.

وضعیت فعلی Tracking.

FPS.

وضعیت ژست‌های دست راست.

وضعیت کلیک‌های دست چپ.

پنل راهنما و اطلاعات ژست‌ها.
میانبرهای کیبورد نیز در همین پنجره دریافت می‌شوند.

پنجره Settings

این پنجره امکان تغییر زنده تنظیمات زیر را می‌دهد:

تنظیم

چه چیزی را تغییر می‌دهد

Pause mouse control

اجرای موقت عملیات ماوس را متوقف می‌کند.

Swap left/right hand

نقش منطقی دست‌های تشخیص داده‌شده را جابه‌جا می‌کند.

Smoothing

مقدار بالاتر حرکت را نرم‌تر می‌کند اما می‌تواند تأخیر بیشتری ایجاد کند.

Pinch sensitivity

تعیین می‌کند دو نوک انگشت چقدر باید به هم نزدیک شوند تا Pinch تشخیص داده شود.

Scroll speed

مقدار اسکرول تولیدشده از حرکت دست را تغییر می‌دهد.

Tracking area size

مشخص می‌کند چه بخشی از تصویر دوربین به کل صفحه نگاشت شود.

Finger-up sensitivity

مشخص می‌کند انگشت چقدر باید بالا باشد تا بالا تشخیص داده شود.

Camera index

دوربین مورد استفاده را انتخاب می‌کند.

تغییرات هنگام اجرای برنامه اعمال می‌شوند.

میانبرهای کیبورد

این میانبرها زمانی کار می‌کنند که پنجره دوربین در حالت Focus باشد.

کلید

عملکرد

P

توقف / ادامه کنترل ماوس

S

نمایش / مخفی کردن پنل راهنما

C

رفتن به دوربین بعدی

Q

خروج

ESC

خروج

برنامه چطور کار می‌کند؟

جریان کلی برنامه به این شکل است:

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
   ├── حرکت نشانگر
   ├── Drag
   ├── Scroll
   ├── Left Click
   └── Right Click
   │
   ▼
Windows Mouse

1. دریافت تصویر دوربین

وب‌کم در یک Thread جداگانه خوانده می‌شود.
به‌جای اینکه حلقه پردازش برای هر cap.read() منتظر بماند، Thread دوربین دائماً جدیدترین فریم موجود را به‌روزرسانی می‌کند. این ساختار کمک می‌کند فریم‌های قدیمی روی هم جمع نشوند و حس تأخیر ورودی کمتر شود.
برنامه رزولوشن تقریبی 640×480 را درخواست می‌کند و در صورت پشتیبانی Backend، تلاش می‌کند Buffer دوربین را کوچک نگه دارد.

2. تشخیص دست

MediaPipe Hand Landmarker جدیدترین فریم RGB دوربین را پردازش می‌کند.
Tracker در حالت VIDEO اجرا می‌شود و امکان تشخیص حداکثر دو دست را دارد.
برای هر دست، نقاط کلیدی مورد نیاز منطق ژست‌ها دریافت می‌شوند.

3. تشخیص چپ و راست

پیش‌نمایش دوربین به‌صورت آینه‌ای نمایش داده می‌شود تا برای کاربر طبیعی‌تر باشد.
چون آینه کردن رابطه چپ و راست را در تصویر تغییر می‌دهد، برنامه برچسب handedness تولیدشده توسط MediaPipe را تنظیم می‌کند و علاوه بر آن گزینه دستی Swap left/right hand را نیز فراهم کرده است.

4. تبدیل حرکت دست به ماوس

مختصات نرمال‌شده نوک انگشت اشاره دست راست از تصویر دوربین گرفته می‌شوند.
محدوده Tracking به مختصات صفحه نمایش تبدیل می‌شود و بعد از اعمال Smoothing، موقعیت نهایی توسط PyAutoGUI به نشانگر واقعی ویندوز داده می‌شود.

5. تشخیص ژست‌ها

برنامه از فاصله بین نقاط کلیدی و وضعیت انگشت‌ها برای تشخیص ژست‌های پشتیبانی‌شده استفاده می‌کند.
برای نمونه:

فاصله شست و اشاره → Drag.

فاصله شست و حلقه → Scroll.

موقعیت انگشت اشاره و وسط → Left / Right Click.

6. مدیریت وضعیت ماوس

برنامه وضعیت Drag و Scroll را در حافظه نگه می‌دارد.
اگر دست راست هنگام Drag ناپدید شود، برنامه دکمه ماوس را آزاد می‌کند و وضعیت Scroll را پاک می‌کند تا ورودی سیستم در حالت گیرکرده باقی نماند.

7. تنظیمات و وضعیت زنده

پنجره Settings با Tkinter ساخته شده و می‌تواند تنظیمات مشترک را در حالی که پردازش دوربین ادامه دارد تغییر دهد.
رابط کاربری همچنین FPS فعلی و وضعیت دوربین را نمایش می‌دهد.

فناوری‌های استفاده‌شده

فناوری

کاربرد

Python

منطق اصلی برنامه

OpenCV

دریافت تصویر و پردازش وب‌کم

MediaPipe Hand Landmarker

تشخیص لحظه‌ای دست و نقاط کلیدی

PyAutoGUI

کنترل ماوس ویندوز

NumPy

نگاشت مختصات و محاسبات عددی

Tkinter

پنجره و کنترل‌های Settings

PyInstaller

ساخت EXE مستقل ویندوز

مدل MediaPipe

این فایل در Repository قرار دارد:

hand_landmarker.task

این فایل همان مدل تشخیص دست MediaPipe است که برنامه برای Tracking از آن استفاده می‌کند.
هنگام اجرای برنامه، وجود مدل در پوشه برنامه بررسی می‌شود. اگر مدل در دسترس نباشد، برنامه می‌تواند آن را از URL تعریف‌شده برای مدل MediaPipe دانلود کند.
در حالت اجرای سورس، بهتر است hand_landmarker.task در کنار main.py قرار داشته باشد.
در Build انجام‌شده با build.bat، دستور PyInstaller فایل مدل را به‌عنوان Data به بسته اضافه می‌کند و Dataهای لازم MediaPipe را نیز جمع‌آوری می‌کند.

اجرای پروژه از سورس

برای اجرا یا توسعه پروژه نیازی به فایل .exe ندارید.

پیش‌نیازها

Windows 10 یا Windows 11

Python

یک وب‌کم سالم

فعال بودن دسترسی دوربین در ویندوز

بسته‌های تعریف‌شده در requirements.txt
برای وابستگی MediaPipe این پروژه، بازه Python 3.10 تا 3.12 نقطه شروع مناسبی است. با این حال، سازگاری دقیق می‌تواند به نسخه بسته‌هایی که هنگام نصب در دسترس هستند بستگی داشته باشد.

1. بررسی نسخه Python

python --version

2. نصب وابستگی‌ها

python -m pip install -r requirements.txt

3. اجرای برنامه

python main.py

پس از اجرا باید دو پنجره باز شوند:

پنجره دوربین و Tracking

پنجره Settings

ساخت فایل EXE مستقل

فایل زیر در پروژه قرار دارد:

build.bat

می‌توانید روی آن دوبار کلیک کنید یا از Command Prompt اجرا کنید:

build.bat

اسکریپت Build این مراحل را انجام می‌دهد:

نصب وابستگی‌های Python.

نصب PyInstaller.

حذف build، dist و فایل .spec قبلی در صورت وجود.

ساخت فایل اجرایی PyInstaller one-file.

اعمال آیکون برنامه.

اضافه کردن hand_landmarker.task.

جمع‌آوری Dataهای MediaPipe.

قرار دادن ماژول‌های Tkinter مورد استفاده Settings.
فایل نهایی در مسیر زیر ساخته می‌شود:

dist\HandMouseControl.exe

استفاده از EXE

فایل اجرایی برای کاربران ویندوزی مناسب است که نمی‌خواهند Python را جداگانه نصب و وابستگی‌ها را مدیریت کنند.
در این پروژه، سورس و نسخه کامپایل‌شده از هم جدا نگه داشته شده‌اند:

GitHub Repository
├── Source code
├── Model
├── Build script
└── Documentation
GitHub Release
└── HandMouseControl.exe

نسخه فعلی از بخش Releases مخزن قابل دریافت است.

ساختار پروژه

HandMouseControl/
├── main.py
├── build.bat
├── requirements.txt
├── hand_landmarker.task
├── icon.ico
├── README.md
└── README.fa.md

فایل

کاربرد

main.py

منطق کامل برنامه

build.bat

اسکریپت خودکار ساخت EXE

requirements.txt

وابستگی‌های Python

hand_landmarker.task

مدل تشخیص دست MediaPipe

icon.ico

آیکون برنامه ویندوز

README.md

مستندات انگلیسی

README.fa.md

مستندات فارسی

معماری برنامه

پروژه از چند بخش اصلی در زمان اجرا تشکیل شده است.

Config

تنظیمات مشترک زمان اجرا را نگه می‌دارد؛ از جمله Smoothing، آستانه Pinch، سرعت Scroll، شماره دوربین، حاشیه Tracking، تعویض دست‌ها، وضعیت Pause، FPS و وضعیت دوربین.

CameraStream

ارتباط با وب‌کم را مدیریت می‌کند و دریافت فریم‌ها را در یک Thread جداگانه انجام می‌دهد.

HandMouseController

Tracker مربوط به MediaPipe را می‌سازد و منطق تبدیل دست به ماوس را در خود نگه می‌دارد.
وظایف این بخش شامل موارد زیر است:

تشخیص نقش دست‌ها

نگاشت مختصات

Smoothing

تشخیص ژست

کلیک

Drag

Scroll

پاک‌سازی وضعیت ورودی

SettingsWindow

رابط Tkinter را می‌سازد و تنظیمات کاربر را با برنامه در حال اجرا هماهنگ می‌کند.

حلقه دوربین

حلقه اصلی پردازش دوربین تقریباً این مسیر را دنبال می‌کند:

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

پردازش هر فریم در برابر خطا محافظت شده تا یک خطای پردازش به‌تنهایی باعث توقف فوری کل حلقه نشود.

مقادیر پیش‌فرض تنظیمات

برنامه با مقادیر اصلی زیر شروع می‌شود:

گزینه

مقدار پیش‌فرض

Camera index

0

Maximum camera indexes

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

غیرفعال

Mouse control

فعال

Overlay panel

قابل مشاهده

این مقادیر را می‌توان از طریق پنجره Settings در زمان اجرا تغییر داد.

عیب‌یابی

<details>
<summary><strong> برنامه اجرا نمی‌شود</strong></summary>
نسخه سورس را از Command Prompt اجرا کنید:

python main.py

با این کار خطای واقعی Python یا مشکل وابستگی‌ها را می‌بینید و مشکل پشت یک EXE گرافیکی پنهان نمی‌ماند.
اگر نسخه Python بدون مشکل اجرا شد ولی EXE اجرا نشد، با build.bat دوباره EXE را بسازید.

</details>

<details>
<summary><strong> دوربین سیاه است یا شناسایی نمی‌شود</strong></summary>
به این مسیر در ویندوز بروید:

Windows Settings → Privacy & security → Camera و مطمئن شوید دسترسی دوربین فعال است.
اگر چند دوربین دارید:

در پنجره دوربین کلید C را بزنید، یا

مقدار Camera index را در Settings تغییر دهید.
همچنین مطمئن شوید برنامه دیگری هم‌زمان وب‌کم را اشغال نکرده باشد.

</details>

<details>
<summary><strong> نشانگر بیش از حد لرزش دارد</strong></summary>
مقدار **Smoothing** را افزایش دهید.
Smoothing بیشتر حرکات ریز را کاهش می‌دهد، اما می‌تواند کمی تأخیر ایجاد کند.

</details>

<details>
<summary><strong> نشانگر با تأخیر حرکت می‌کند</strong></summary>
مقدار **Smoothing** را کاهش دهید.
همچنین بررسی کنید برنامه دیگری از وب‌کم استفاده نکند یا فشار پردازشی اضافی روی سیستم ایجاد نکند.

</details>

<details>
<summary><strong> Pinchها درست تشخیص داده نمی‌شوند</strong></summary>
مقدار **Pinch sensitivity** را تنظیم کنید.
اگر Pinch بیش از حد راحت فعال می‌شود، حساسیت را در جهت مخالف تغییر دهید. اگر تقریباً هیچ‌وقت فعال نمی‌شود، حساسیت را بیشتر کنید تا با فاصله دست و شرایط نور دوربین شما مناسب شود.

</details>

<details>
<summary><strong> ژست‌های کلیک بیش از حد حساس یا کم‌حساس هستند</strong></summary>
مقدار **Finger-up sensitivity** را در Settings تغییر دهید.
این گزینه مشخص می‌کند نوک انگشت چقدر باید از مفصل خود بالاتر باشد تا به‌عنوان انگشت بالا تشخیص داده شود.

</details>

<details>
<summary><strong> دست چپ و راست اشتباه تشخیص داده می‌شوند</strong></summary>
گزینه زیر را فعال کنید:

Swap left/right hand

در پنجره Settings.

</details>

<details>
<summary><strong> MediaPipe بعد از Build Import نمی‌شود</strong></summary>
با استفاده از `build.bat` پروژه را دوباره Build کنید.
دستور Build، Dataهای MediaPipe را به‌صورت صریح جمع‌آوری می‌کند و فایل مدل مورد نیاز برنامه را نیز اضافه می‌کند.

</details>

<details>
<summary><strong> مدل Hand Landmarker دانلود نمی‌شود</strong></summary>
اگر `hand_landmarker.task` وجود نداشته باشد، برنامه می‌تواند تلاش کند آن را دانلود کند.
این موارد را بررسی کنید:

اتصال اینترنت

محدودیت Firewall

امکان دسترسی برنامه به URL مدل MediaPipe
در حالت اجرای سورس می‌توانید از فایل hand_landmarker.task موجود در پروژه نیز استفاده کنید.

</details>

<details>
<summary><strong> نصب MediaPipe با خطا مواجه می‌شود</strong></summary>
فایل Requirements به‌جای یک نسخه کاملاً ثابت، از بازه نسخه‌ها استفاده می‌کند.
ابتدا نسخه Python را بررسی کنید:

python --version

محیط Python 3.10 تا 3.12 برای شروع این پروژه انتخاب مناسبی است.

</details>

<details>
<summary><strong> فایل EXE در اجرای اولیه کمی دیر باز می‌شود</strong></summary>
EXE با حالت PyInstaller `--onefile` ساخته می‌شود و هنگام شروع باید فایل‌های بسته‌بندی‌شده را استخراج کند.
بنابراین کمی تأخیر در شروع می‌تواند طبیعی باشد.

</details>

حریم خصوصی

این برنامه از وب‌کم برای Tracking لحظه‌ای دست و کنترل ماوس استفاده می‌کند.
پروژه به‌صورت عمدی فریم‌های دوربین یا نتایج Tracking دست را به یک سرویس آنلاین ارسال نمی‌کند.
پردازش دوربین بخشی از جریان اجرای محلی برنامه است.
دسترسی اینترنت ممکن است برای موارد زیر لازم باشد:

نصب بسته‌های Python

دانلود مدل MediaPipe در صورت نبودن آن به‌صورت محلی

امنیت

فقط سورس کد یا فایل اجرایی را از نسخه‌ای اجرا کنید که به آن اعتماد دارید.
از آنجا که برنامه به وب‌کم دسترسی دارد و می‌تواند ماوس ویندوز را کنترل کند، قبل از اجرا باید کد یا فایل اجرایی مورد استفاده را بشناسید و به آن اعتماد داشته باشید.
برنامه‌های ساخته‌شده با PyInstaller ممکن است در بعضی آنتی‌ویروس‌ها یا سیستم‌های Reputation هشدار ایجاد کنند. چنین هشداری را نباید بدون بررسی نادیده گرفت.
اگر به فایل آماده اعتماد ندارید، می‌توانید EXE را مستقیماً از همین Source Code خودتان Build کنید.

توسعه

Repository همه فایل‌های لازم برای بررسی، تغییر، تست و Build دوباره برنامه را در اختیار قرار می‌دهد.
یک جریان کاری ساده برای توسعه:

python --version
python -m pip install -r requirements.txt
python main.py

بعد از اعمال تغییرات:

build.bat

فایل اجرایی جدید در این مسیر ساخته می‌شود:

dist\HandMouseControl.exe

نکات مفید برای توسعه

قبل از بررسی منطق ژست، ابتدا دسترسی به دوربین را تست کنید.

برای تست میانبرهای کیبورد، پنجره دوربین را در حالت Focus نگه دارید.

Smoothing و حساسیت ژست‌ها را با شرایط واقعی وب‌کم خود تنظیم کنید.

Tracking یک دست و دو دست را هر دو تست کنید.

حالتی را که دست هنگام Drag ناپدید می‌شود نیز آزمایش کنید.

مشارکت در پروژه

مشارکت در پروژه آزاد است.
روش معمول:

Repository را Fork کنید.

تغییرات خود را اعمال کنید.

برنامه را از سورس اجرا کنید.

رفتار دوربین و ژست‌ها را تست کنید.

یک Pull Request ارسال کنید.

گزارش Bug

هنگام گزارش مشکل، تا حد امکان اطلاعات زیر را اضافه کنید:

نسخه Windows

نسخه Python

مدل دوربین در صورت مرتبط بودن

ژستی که استفاده می‌کردید

چیزی که انتظار داشتید اتفاق بیفتد

اتفاقی که واقعاً افتاد

متن خطا در صورت وجود

مراحلی که مشکل را دوباره ایجاد می‌کنند

Releases

Repository فایل‌های توسعه و برنامه کامپایل‌شده ویندوز را از یکدیگر جدا نگه می‌دارد.

مخزن Source

شامل موارد زیر است:

سورس Python

Requirements

مدل MediaPipe

Build script

آیکون

مستندات فارسی و انگلیسی

GitHub Releases

شامل نسخه آماده اجرای برنامه برای ویندوز است.
نسخه فعلی:

Hand Mouse Control v1.0.0 مشاهده Releases →

License

در حال حاضر هیچ لایسنس متن‌باز مشخصی به این پروژه اضافه نشده است.
تا زمانی که یک License واقعی به Repository اضافه نشود، نباید فرض کرد سورس کد برای استفاده، تغییر یا انتشار مجدد تحت یک لایسنس Open Source قرار دارد.

ارتباط

برای سؤال، گزارش خطا، پیشنهاد یا بازخورد:

Telegram: @XRO_G

<div align="center">

ساخته‌شده با Python، OpenCV، MediaPipe، PyAutoGUI و Tkinter.

 Repository ·  Releases ·  Telegram

English · فارسی </div>
