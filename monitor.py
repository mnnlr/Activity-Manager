import tkinter as tk
from login import LoginPage
from success import SuccessPage
from logout import logout
from action import UserActivityMonitor

# Global variables to hold the page instances and tokens
login_page = None
success_page = None
tokens = {}

def show_login_page():
    global login_page, success_page, is_auth
    is_auth = False
    if login_page:
        login_page.frame.destroy()
    if success_page:
        success_page.frame.destroy()
    login_page = LoginPage(root, on_login_success)

def show_success_page(tokens):
    global success_page
    success_page = SuccessPage(root, tokens, handle_logout)

def on_login_success(tokens_param):
    global is_auth, tokens
    is_auth = True
    tokens = tokens_param  # Update global tokens variable
    login_page.frame.destroy()
    show_success_page(tokens_param)
    # Start monitoring user activity after login
    UserActivityMonitor(on_inactivity=handle_logout)

def handle_logout():
    global is_auth, tokens, success_page
    if is_auth:
        print("Logging out...")
        if 'access_token' in tokens:  # Check if access_token exists in tokens
            logout(tokens['access_token'], show_login_page)
        else:
            print("No access_token found in tokens.")
        is_auth = False
        if success_page:
            success_page.frame.destroy()
        show_login_page()

root = tk.Tk()
root.title("Activity Monitor")

# Calculate desired dimensions
normal_width = 1366  # Typical laptop screen width
normal_height = 768  # Typical laptop screen height

desired_width = normal_width // 2
desired_height = (normal_height * 3) // 4

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = (screen_width - desired_width) // 2
y_cordinate = (screen_height - desired_height) // 2

# Set the window geometry
root.geometry(f"{desired_width}x{desired_height}+{x_cordinate}+{y_cordinate}")

is_auth = False


show_login_page()


root.mainloop()

