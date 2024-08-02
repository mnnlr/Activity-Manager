from kivy.uix.screenmanager import Screen
from action import UserActivityMonitor
from logout_action import perform_logout

class SuccessScreen(Screen):
    def __init__(self, perform_logout, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.user_data = {}
        self.perform_logout = perform_logout
        self.screen_manager = screen_manager
        self.user_activity_monitor = None
    def on_enter(self):
        self.user_activity_monitor = UserActivityMonitor(on_inactivity=self.logout_due_to_inactivity)
    def on_leave(self):
        if self.user_activity_monitor:
            self.user_activity_monitor.stop_monitoring()
            self.user_activity_monitor = None

    def logout_due_to_inactivity(self):
        print("User has been logged out due to inactivity")
        cookie = self.screen_manager.get_screen('login').cookies
        #access_token = self.user_data.get('access_token')

        def on_success():
            print("Logout Successful")
            self.screen_manager.current = 'login'
            login_screen = self.screen_manager.get_screen('login')
            login_screen.clear_fields()

        def on_failure(message):
            print(message)

        if cookie:
            self.perform_logout(cookie, on_success, on_failure)
        else:
            self.screen_manager.current = 'login'
            login_screen = self.screen_manager.get_screen('login')
            login_screen.clear_fields()
