import tkinter as tk
from tkinter import messagebox
import requests

class LoginPage:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.frame = tk.Frame(root, bd=5, relief=tk.GROOVE)
        self.frame.pack(pady=50)
        
        self.label_username = tk.Label(self.frame, text="Username")
        self.label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(self.frame, text="Password")
        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.button_login = tk.Button(self.frame, text="Login", command=self.login)
        self.button_login.grid(row=2, columnspan=2, pady=10)

        self.tokens = {}

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            response = requests.post(
                'http://127.0.0.1:5000/login',
                json={'username': username, 'password': password}
            )
            response_data = response.json()

            if response.status_code == 200 and response_data.get('message') == 'Login Success':
                messagebox.showinfo("Login", "Login Successful")

                # Store tokens for further use
                self.tokens['access_token'] = response_data.get('access_token')
                self.tokens['refresh_token'] = response_data.get('refresh_token')

                self.on_success(self.tokens)
            else:
                messagebox.showerror("Login", response_data.get('message', 'Login Failed'))
        
        except requests.RequestException as e:
            messagebox.showerror("Login", f"An error occurred: {e}")

    def get_tokens(self):
        return self.tokens
