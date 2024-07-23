import tkinter as tk
from logout import logout

class SuccessPage:
    def __init__(self, root, tokens, on_logout):
        self.root = root
        self.tokens = tokens
        self.on_logout = on_logout
        self.frame = tk.Frame(root, bd=5, relief=tk.GROOVE)
        self.frame.pack(pady=50)

        self.label_success = tk.Label(self.frame, text="Profile",)
        self.label_success.grid(row=0, column=1, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="Name:")
        self.label_success.grid(row=1, column=0, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="Deepak")
        self.label_success.grid(row=1, column=2, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="Employee ID")
        self.label_success.grid(row=2, column=0, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="1")
        self.label_success.grid(row=2, column=2, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="Position")
        self.label_success.grid(row=3, column=0, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="Software Engineer")
        self.label_success.grid(row=3, column=2, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="Department")
        self.label_success.grid(row=4, column=0, padx=10, pady=10)
        self.label_success = tk.Label(self.frame, text="Engineering")
        self.label_success.grid(row=4, column=2, padx=10, pady=10)
        self.button_logout = tk.Button(self.frame, text="Logout", command=on_logout)
        self.button_logout.grid(row=5, column=1, pady=10)

