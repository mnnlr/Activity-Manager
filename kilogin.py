from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import requests
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

class LoginScreen(Screen):
    def userlogin(self, username, password):
        print(f"Attempting to log in with username: {username}, password: {password}")
        tokens = {}
        try:
            response = requests.post(
                'http://127.0.0.1:5000/login',
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'}
            )
            
            response_data = response.json()

            if response.status_code == 200 and response_data.get('message') == 'Login Success':
                tokens['access_token'] = response_data.get('access_token')
                tokens['refresh_token'] = response_data.get('refresh_token')
                self.manager.get_screen('success').tokens = tokens
                self.show_dialog("Login", response_data.get('message', 'Login Success'))  # Store tokens in SuccessScreen
                self.manager.current = 'success'
                self.clear_fields()  # Clear username and password fields after successful login
            else:
                self.show_dialog("Login", response_data.get('message', 'Login Failed'))
        
        except requests.RequestException as e:
            self.show_dialog("Login", f"An error occurred: {e}")

    def clear_fields(self):
        self.ids.user.text = ''
        self.ids.password.text = ''

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

class SuccessScreen(Screen):
    tokens = {}

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        Builder.load_file('login.kv')
        Builder.load_file('detailspage.kv')
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(SuccessScreen(name='success'))
        return self.screen_manager

    def login(self):
        print("Login button pressed")
        login_screen = self.screen_manager.get_screen('login')
        username = login_screen.ids.user.text
        password = login_screen.ids.password.text
        print(f"Username: {username}, Password: {password}")
        login_screen.userlogin(username, password)

    def logout(self):
        print("Logout button pressed")
        access_token = self.screen_manager.get_screen('success').tokens.get('access_token')
        self.perform_logout(access_token, self.on_logout)

    def perform_logout(self, access_token, on_logout):
        try:
            response = requests.post(
                'http://127.0.0.1:5000/logout',
                headers={'Authorization': f'Bearer {access_token}'}
            )

            if response.status_code == 200:
                self.show_message("Logout", "Logout Successful")
                on_logout()
            else:
                self.show_message("Logout", "Logout Failed")
        except requests.RequestException as e:
            self.show_message("Logout", f"An error occurred: {e}")

    def show_message(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def on_logout(self):
        login_screen = self.screen_manager.get_screen('login')
        login_screen.clear_fields()  
        self.screen_manager.current = 'login'

if __name__ == '__main__':
    MainApp().run()
