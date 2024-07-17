import requests
from tkinter import messagebox

def logout(access_token, on_logout):
    try:
        response = requests.post(
            'http://127.0.0.1:5000/logout',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if response.status_code == 200:
            messagebox.showinfo("Logout", "Logout Successful")
            on_logout()
        else:
            messagebox.showerror("Logout", "Logout Failed")
    except requests.RequestException as e:
        messagebox.showerror("Logout", f"An error occurred: {e}")
