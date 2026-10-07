import math
import os
import sys
import threading
import time
import urllib.request

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import ttk
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
MODEL_NAME = "hand_landmarker.task"

THUMB_TIP = 4
INDEX_TIP = 8
INDEX_PIP = 6
MIDDLE_TIP = 12
MIDDLE_PIP = 10
RING_TIP = 16
RING_PIP = 14
PINKY_TIP = 20
PINKY_PIP = 18

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
SCREEN_W, SCREEN_H = pyautogui.size()


class Config:
    def __init__(self):
        self.camera_index = 0
        self.max_cameras = 4
        self.frame_margin = 0.15
        self.smoothing = 0.35
        self.pinch_threshold = 0.045
        self.scroll_speed = 800
        self.finger_margin = 0.02
        self.swap_hands = False
        self.paused = False
        self.show_overlay = True
        self.fps = 0.0
        self.camera_ok = False


CONFIG = Config()


def base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def model_path():
    if getattr(sys, "frozen", False):
        bundled = os.path.join(getattr(sys, "_MEIPASS", ""), MODEL_NAME)
        if os.path.isfile(bundled):
            return bundled
    return os.path.join(base_dir(), MODEL_NAME)


def ensure_model():
    path = model_path()
    if os.path.isfile(path):
        return path

    target = os.path.join(base_dir(), MODEL_NAME)
    try:
        urllib.request.urlretrieve(MODEL_URL, target)
    except Exception as exc:
        raise RuntimeError(f"Could not get the hand model: {exc}") from exc
    return target


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def clamp(value, low, high):
    return max(low, min(high, value))


class CameraStream:
    def __init__(self, index):
        self.lock = threading.Lock()
        self.cap = None
        self.frame = None
        self.ok = False
        self.index = index
        self.stopped = False
        self._open(index)
        self.thread = threading.Thread(target=self._read_loop, daemon=True)
        self.thread.start()

    def _open(self, index):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            cap = cv2.VideoCapture(index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        with self.lock:
            self.cap = cap
            self.index = index
            self.ok = False
            self.frame = None

    def switch(self, index):
        with self.lock:
            old_cap = self.cap
            self.cap = None
        if old_cap is not None:
            old_cap.release()
        self._open(index)

    def _read_loop(self):
        while not self.stopped:
            with self.lock:
                cap = self.cap
            if cap is None:
                time.sleep(0.05)
                continue

            try:
                ok, frame = cap.read()
            except Exception:
                ok, frame = False, None

            with self.lock:
                if cap is self.cap:
                    self.ok = ok
                    if ok:
                        self.frame = frame

            if not ok:
                time.sleep(0.02)

    def read(self):
        with self.lock:
            frame = None if self.frame is None else self.frame.copy()
            return self.ok, frame

    def stop(self):
        self.stopped = True
        self.thread.join(timeout=1)
        with self.lock:
            cap = self.cap
            self.cap = None
        if cap is not None:
            cap.release()


class HandMouseController:
    def __init__(self, config, model):
        self.config = config
        options = vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.6,
            min_tracking_confidence=0.6,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.prev_x, self.prev_y = pyautogui.position()
        self.dragging = False
        self.scrolling = False
        self.scroll_y = None
        self.left_latched = False
        self.right_latched = False

    def detect(self, frame, timestamp):
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        return self.landmarker.detect_for_video(image, timestamp)

    def hand_side(self, label):
        side = "Left" if label == "Right" else "Right"
        if self.config.swap_hands:
            side = "Left" if side == "Right" else "Right"
        return side

    def screen_position(self, x, y):
        margin = self.config.frame_margin
        sx = np.interp(x, [margin, 1 - margin], [0, SCREEN_W])
        sy = np.interp(y, [margin, 1 - margin], [0, SCREEN_H])
        return clamp(sx, 0, SCREEN_W - 1), clamp(sy, 0, SCREEN_H - 1)

    def smooth(self, x, y):
        amount = self.config.smoothing
        self.prev_x = self.prev_x * amount + x * (1 - amount)
        self.prev_y = self.prev_y * amount + y * (1 - amount)
        return self.prev_x, self.prev_y

    def fingers_up(self, landmarks):
        margin = self.config.finger_margin
        index = landmarks[INDEX_TIP].y < landmarks[INDEX_PIP].y - margin
        middle = landmarks[MIDDLE_TIP].y < landmarks[MIDDLE_PIP].y - margin
        ring = landmarks[RING_TIP].y < landmarks[RING_PIP].y - margin
        pinky = landmarks[PINKY_TIP].y < landmarks[PINKY_PIP].y - margin
        return index, middle, ring, pinky

    def right_hand(self, landmarks):
        thumb = landmarks[THUMB_TIP]
        index = landmarks[INDEX_TIP]
        ring = landmarks[RING_TIP]
        drag = distance(thumb, index) < self.config.pinch_threshold
        scroll = distance(thumb, ring) < self.config.pinch_threshold

        x, y = self.screen_position(index.x, index.y)
        x, y = self.smooth(x, y)

        if self.config.paused:
            return {"drag": drag, "scroll": scroll}

        if scroll:
            if not self.scrolling:
                self.scrolling = True
                self.scroll_y = index.y
            else:
                amount = (index.y - self.scroll_y) * self.config.scroll_speed
                pyautogui.scroll(int(-amount))
                self.scroll_y = index.y
            return {"drag": drag, "scroll": True}

        self.scrolling = False
        self.scroll_y = None
        pyautogui.moveTo(x, y)

        if drag and not self.dragging:
            pyautogui.mouseDown()
            self.dragging = True
        elif not drag and self.dragging:
            pyautogui.mouseUp()
            self.dragging = False

        return {"drag": drag, "scroll": False}

    def left_hand(self, landmarks):
        index, middle, ring, pinky = self.fingers_up(landmarks)
        count = sum((index, middle, ring, pinky))
        right_click = index and count == 1
        left_click = index and middle and count == 2

        if not self.config.paused:
            if right_click and not self.right_latched:
                pyautogui.click(button="right")
            if left_click and not self.left_latched:
                pyautogui.click(button="left")

        self.right_latched = right_click
        self.left_latched = left_click
        return {"right_click": right_click, "left_click": left_click}

    def reset_right(self):
        if self.dragging:
            pyautogui.mouseUp()
            self.dragging = False
        self.scrolling = False
        self.scroll_y = None

    def reset_left(self):
        self.right_latched = False
        self.left_latched = False

    def close(self):
        if self.dragging:
            pyautogui.mouseUp()
        self.landmarker.close()


def draw_landmarks(frame, landmarks, color):
    height, width = frame.shape[:2]
    points = [(int(p.x * width), int(p.y * height)) for p in landmarks]
    for start, end in HAND_CONNECTIONS:
        cv2.line(frame, points[start], points[end], color, 2)
    for point in points:
        cv2.circle(frame, point, 4, (255, 255, 255), -1)


def draw_panel(frame, x, y, width, height):
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + width, y + height), (20, 20, 24), -1)
    frame[:] = cv2.addWeighted(overlay, 0.55, frame, 0.45, 0)


def draw_hud(frame, config, gestures, fps):
    height, width = frame.shape[:2]
    draw_panel(frame, 0, 0, 260, 96)

    status = "PAUSED" if config.paused else "ACTIVE"
    status_color = (0, 165, 255) if config.paused else (60, 220, 90)
    cv2.putText(frame, f"Hand Mouse: {status}", (14, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
    cv2.putText(frame, f"{fps:.0f} FPS", (14, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (210, 210, 210), 1)

    right = gestures.get("right")
    text = "no hand"
    if right:
        tags = []
        if right.get("drag"):
            tags.append("DRAG")
        if right.get("scroll"):
            tags.append("SCROLL")
        text = " + ".join(tags) if tags else "move"

    cv2.circle(frame, (22, 72), 6, (255, 200, 0), -1)
    cv2.putText(frame, f"Right hand: {text}", (36, 76), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    if config.show_overlay:
        panel_width = 300
        draw_panel(frame, width - panel_width, 0, panel_width, 96)
        left = gestures.get("left")
        text = "no hand"
        if left:
            tags = []
            if left.get("right_click"):
                tags.append("RIGHT-CLICK")
            if left.get("left_click"):
                tags.append("LEFT-CLICK")
            text = " + ".join(tags) if tags else "idle"

        x = width - panel_width + 16
        cv2.circle(frame, (x, 24), 6, (255, 0, 200), -1)
        cv2.putText(frame, "Left hand (clicks)", (x + 14, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        cv2.putText(frame, text, (x, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        cv2.putText(frame, "1 finger = right-click", (x, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (185, 185, 185), 1)
        cv2.putText(frame, "2 fingers = left-click", (x, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (185, 185, 185), 1)

    cv2.putText(frame, "p:pause  s:legend  c:camera  q:quit", (10, height - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (170, 170, 170), 1)


def camera_loop(config, stop_event, model):
    camera = CameraStream(config.camera_index)
    controller = HandMouseController(config, model)
    window = "Hand Mouse Control"
    cv2.namedWindow(window)

    start = time.time()
    previous = start
    fps = 0.0

    try:
        while not stop_event.is_set():
            if camera.index != config.camera_index:
                camera.switch(config.camera_index)

            ok, frame = camera.read()
            config.camera_ok = ok
            if not ok or frame is None:
                blank = np.zeros((240, 420, 3), dtype=np.uint8)
                cv2.putText(blank, "No camera signal", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.imshow(window, blank)
                key = cv2.waitKey(30) & 0xFF
                if key in (ord("q"), 27):
                    stop_event.set()
                    break
                continue

            gestures = {}
            try:
                frame = cv2.flip(frame, 1)
                rgb = np.ascontiguousarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                timestamp = int((time.time() - start) * 1000)
                result = controller.detect(rgb, timestamp)

                saw_right = False
                saw_left = False

                for landmarks, handedness in zip(result.hand_landmarks, result.handedness):
                    side = controller.hand_side(handedness[0].category_name)
                    color = (255, 200, 0) if side == "Right" else (255, 0, 200)
                    draw_landmarks(frame, landmarks, color)
                    if side == "Right":
                        saw_right = True
                        gestures["right"] = controller.right_hand(landmarks)
                    else:
                        saw_left = True
                        gestures["left"] = controller.left_hand(landmarks)

                if not saw_right:
                    controller.reset_right()
                if not saw_left:
                    controller.reset_left()
            except Exception as exc:
                print(f"frame error: {exc}")

            now = time.time()
            current_fps = 1.0 / max(now - previous, 1e-6)
            previous = now
            fps = current_fps if fps == 0 else fps * 0.9 + current_fps * 0.1
            config.fps = fps

            draw_hud(frame, config, gestures, fps)
            cv2.imshow(window, frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                stop_event.set()
                break
            if key == ord("p"):
                config.paused = not config.paused
            elif key == ord("s"):
                config.show_overlay = not config.show_overlay
            elif key == ord("c"):
                config.camera_index = (config.camera_index + 1) % config.max_cameras
    finally:
        controller.close()
        camera.stop()
        cv2.destroyAllWindows()


class SettingsWindow:
    def __init__(self, root, config, stop_event):
        self.root = root
        self.config = config
        self.stop_event = stop_event

        root.title("Hand Mouse Control - Settings")
        root.geometry("360x460")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.status = tk.StringVar(value="Starting...")
        ttk.Label(root, textvariable=self.status, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=14, pady=6)

        self.paused = tk.BooleanVar(value=config.paused)
        ttk.Checkbutton(root, text="Pause mouse control", variable=self.paused, command=self.sync_paused).pack(anchor="w", padx=14, pady=6)

        self.swap = tk.BooleanVar(value=config.swap_hands)
        ttk.Checkbutton(root, text="Swap left/right hand", variable=self.swap, command=self.sync_swap).pack(anchor="w", padx=14, pady=6)

        self.add_slider(root, "Smoothing", "smoothing", 0.0, 0.95, 0.01)
        self.add_slider(root, "Pinch sensitivity", "pinch_threshold", 0.015, 0.12, 0.005)
        self.add_slider(root, "Scroll speed", "scroll_speed", 100, 2500, 50)
        self.add_slider(root, "Tracking area size", "frame_margin", 0.0, 0.4, 0.01)
        self.add_slider(root, "Finger-up sensitivity", "finger_margin", 0.0, 0.06, 0.002)

        row = ttk.Frame(root)
        row.pack(anchor="w", fill="x", padx=14, pady=6)
        ttk.Label(row, text="Camera index:").pack(side="left")
        self.camera = tk.IntVar(value=config.camera_index)
        ttk.Spinbox(row, from_=0, to=config.max_cameras - 1, width=4, textvariable=self.camera, command=self.sync_camera).pack(side="left", padx=6)

        ttk.Label(
            root,
            text="Right hand: move, pinch thumb+index to drag, pinch thumb+ring to scroll.\nLeft hand: 1 finger = right-click, 2 fingers = left-click.",
            justify="left",
            foreground="#555",
        ).pack(anchor="w", padx=14, pady=6)

        ttk.Button(root, text="Quit", command=self.close).pack(pady=14)
        self.update_status()

    def add_slider(self, parent, label, name, low, high, step):
        frame = ttk.Frame(parent)
        frame.pack(anchor="w", fill="x", padx=14, pady=4)
        ttk.Label(frame, text=label, width=18).pack(side="left")

        variable = tk.DoubleVar(value=getattr(self.config, name))
        value = ttk.Label(frame, width=6)
        value.pack(side="right")

        def changed(_=None):
            number = variable.get()
            setattr(self.config, name, number)
            value.config(text=f"{number:.0f}" if step >= 1 else f"{number:.3f}")

        ttk.Scale(frame, from_=low, to=high, orient="horizontal", variable=variable, command=changed).pack(side="left", fill="x", expand=True, padx=6)
        changed()

    def sync_paused(self):
        self.config.paused = self.paused.get()

    def sync_swap(self):
        self.config.swap_hands = self.swap.get()

    def sync_camera(self):
        self.config.camera_index = self.camera.get()

    def update_status(self):
        status = "PAUSED" if self.config.paused else "ACTIVE"
        camera = "camera OK" if self.config.camera_ok else "no camera signal"
        self.status.set(f"{status}  |  {self.config.fps:.0f} FPS  |  {camera}")
        if not self.stop_event.is_set():
            self.root.after(200, self.update_status)
        else:
            self.root.destroy()

    def close(self):
        self.stop_event.set()
        self.root.destroy()


def main():
    model = ensure_model()
    stop_event = threading.Event()

    camera_thread = threading.Thread(target=camera_loop, args=(CONFIG, stop_event, model), daemon=True)
    camera_thread.start()

    root = tk.Tk()
    SettingsWindow(root, CONFIG, stop_event)
    root.mainloop()

    stop_event.set()
    camera_thread.join(timeout=2)


if __name__ == "__main__":
    main()
