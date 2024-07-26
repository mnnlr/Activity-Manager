# main.py
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from login_screen import LoginScreen
from success_screen import SuccessScreen
from logout_action import perform_logout  # Import the function here

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        Builder.load_file('login.kv')
        Builder.load_file('detailspage.kv')
        self.screen_manager = ScreenManager()
        # Pass the 'screen_manager' and 'perform_logout' to SuccessScreen
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(SuccessScreen(name='success', perform_logout=perform_logout, screen_manager=self.screen_manager))
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

        def on_success():
            self.show_message("Logout", "Logout Successful")
            self.on_logout()  # Clear fields and navigate to login screen

        def on_failure(message):
            self.show_message("Logout", message)

        perform_logout(access_token, on_success, on_failure)

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
        login_screen.clear_fields()  # Clear fields
        self.screen_manager.current = 'login'

if __name__ == '__main__':
    MainApp().run()
