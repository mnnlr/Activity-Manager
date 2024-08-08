import pyautogui
from pynput import mouse, keyboard
import threading
import time
from kivy.clock import Clock

class UserActivityMonitor:
    def __init__(self, on_inactivity):
        self.on_inactivity = on_inactivity
        self.last_activity_time = time.time()
        self.inactivity_threshold = 2700
        self.monitoring_active = True 

        self.monitor_thread = threading.Thread(target=self.monitor_activity)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity, on_scroll=self.on_activity)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def on_activity(self, *args):
        self.last_activity_time = time.time()

    def stop_monitoring(self):
        self.monitoring_active = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def monitor_activity(self):
        while self.monitoring_active:
            current_time = time.time()
            if current_time - self.last_activity_time > self.inactivity_threshold:
                Clock.schedule_once(lambda dt: self.on_inactivity())
                self.stop_monitoring() 
            time.sleep(1)
