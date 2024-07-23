import pyautogui
from pynput import mouse, keyboard
import threading
import time

class UserActivityMonitor:
    def __init__(self, on_inactivity):
        self.on_inactivity = on_inactivity
        self.last_activity_time = time.time()
        self.inactivity_threshold = 10 


        self.monitor_thread = threading.Thread(target=self.monitor_activity)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()


        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity, on_scroll=self.on_activity)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def on_activity(self, *args):
        self.last_activity_time = time.time()

    def monitor_activity(self):
        while True:
            current_time = time.time()
            if current_time - self.last_activity_time > self.inactivity_threshold:
                self.on_inactivity()
                self.last_activity_time = current_time  
            time.sleep(1) 
            
            
           
