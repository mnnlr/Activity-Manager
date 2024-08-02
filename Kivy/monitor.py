from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import ScreenManager
from login_screen import LoginScreen
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from success_screen import SuccessScreen
from kivymd.uix.label import MDLabel
from logout_action import perform_logout  
from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.datatables import MDDataTable
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from datetime import datetime



class ProfileCard(MDCard):
    name = StringProperty("")
    email = StringProperty("")
    phone_number = StringProperty("")
    address = StringProperty("")

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        Builder.load_file('login.kv')
        Builder.load_file('success.kv')
        self.screen_manager = ScreenManager()
        
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(SuccessScreen(name='success', perform_logout=perform_logout, screen_manager=self.screen_manager))
        return self.screen_manager

    def login(self):
        print("Login button pressed")
        login_screen = self.screen_manager.get_screen('login')
        username = login_screen.ids.user.text
        password = login_screen.ids.password.text
        print(f"Username: {username}, Password: {password}")

        login_screen.userlogin(username, password,self.display_table)

    def logout(self):
        print("Logout button pressed")
        access_token = self.screen_manager.get_screen('success').user_data.get('access_token')
        cookie = self.screen_manager.get_screen('login').cookies


        def on_success():
            self.show_message("Logout", "Logout Successful")
            self.on_logout()  

        def on_failure(message):
            self.show_message("Logout", message)

        perform_logout(cookie, on_success, on_failure)

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

    def display_table(self):
        success_screen = self.screen_manager.get_screen('success')
        success_screen.ids.widget.text = "Attendence"
        if not hasattr(self, 'attendance_table'):
            scroll_container = success_screen.ids.scroll_container
            scroll_container.clear_widgets()
            login_screen = self.screen_manager.get_screen('login')
            attendance_data = login_screen.get_attendance_data()

            if not attendance_data or not attendance_data.get('success'):
                print("No attendance data available.")
                return

            data = attendance_data.get('Data', {})
            time_tracking = data.get('timeTracking', [])

            formatted_data = [
                (str(index + 1), entry.get('timeIn', 'N/A'),
                 entry.get('timeOut','N/A') if index != 0 else 'Working Now'
                 , entry.get('duration', 'N/A'))
                for index, entry in enumerate(time_tracking)
            ]

            table = MDDataTable(
                size_hint=(1, None),
                height=dp(330),
                rows_num=len(time_tracking),
                column_data=[
                    ("Login Count", dp(40)),
                    ("Login Time", dp(40)),
                    ("Logout Time", dp(40)),
                    ("Duration", dp(40))
                ],
                row_data=formatted_data
            )
            self.attendance_table = table
            scroll_container.add_widget(table)
        else:
            success_screen.ids.scroll_container.clear_widgets()
            success_screen.ids.scroll_container.add_widget(self.attendance_table)
    def display_employeeinfo(self):
        success_screen = self.screen_manager.get_screen('success')
        success_screen.ids.widget.text = "Employee Info"
        if not hasattr(self, 'employee_info_card'):
            scroll_container = success_screen.ids.scroll_container
            scroll_container.clear_widgets()
            
            login_screen = self.screen_manager.get_screen('login')
            employee_data = login_screen.get_employee_data()
            
            card = MDCard(
                size_hint=(None, None),
                size=(dp(869), dp(330)),
                orientation='vertical',
                padding=dp(5),
                spacing=dp(5),
                pos_hint={'center_x': 0.3},
                #elevation=10,  
                #md_bg_color=(0.9, 0.9, 0.9, 1) 
            )

            grid_layout = GridLayout(
                cols=2,
                size_hint_y=None,
                height=dp(300),
                padding=dp(5),
                spacing=dp(5)
            )

            keys_to_display = ['employeeId', 'createdAt', 'designation', 'designationLevel', 'Shift']
            for key in keys_to_display:
                value = employee_data.get(key, 'N/A')
                if key == 'createdAt' and 'T' in value:
                    try:
                        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
                    except ValueError as e:
                        print(f"Error parsing date: {e}")
                        value = "Unknown"

                label_key = MDLabel(
                    text=key.replace('_', ' ').title() + ':',
                    size_hint_y=None,
                    height=dp(40),
                    halign='center',
                    valign='middle',
                    font_style='Subtitle1',  
                    color=(0, 0, 0, 1)  
                )
                label_value = MDLabel(
                    text=value,
                    size_hint_y=None,
                    height=dp(40),
                    halign='center',
                    valign='middle',
                    font_style='Subtitle1',  
                    color=(0.3, 0.3, 0.3, 1)  
                )

                grid_layout.add_widget(label_key)
                grid_layout.add_widget(label_value)

            card.add_widget(grid_layout)

            empty_widget = Widget(
                size_hint_y=None,
                height=dp(20)
            )
            card.add_widget(empty_widget)

            self.employee_info_card = card
            scroll_container.add_widget(card)
        else:
            success_screen.ids.scroll_container.clear_widgets()
            success_screen.ids.scroll_container.add_widget(self.employee_info_card)


    def display_personalinfo(self):
        success_screen = self.screen_manager.get_screen('success')
        success_screen.ids.widget.text = "Personal Information"
        if not hasattr(self, 'personal_info_card'):
            scroll_container = success_screen.ids.scroll_container
            scroll_container.clear_widgets()
            login_screen = self.screen_manager.get_screen('login')
            employee_data = login_screen.get_employee_data()

            card = MDCard(
                size_hint=(None, None),
                size=(dp(869), dp(330)),
                orientation='vertical',
                padding=dp(5),
                spacing=dp(5),
                pos_hint={'center_x': 0.5},
               # elevation=10,  
                #md_bg_color=(0.9, 0.9, 0.9, 1) 
            )
            scroll_view = ScrollView(
                size_hint=(1, 1),
                size=(dp(869), dp(330)),  
                do_scroll_x=False,
                pos_hint={'center_x': 0.5},
                do_scroll_y=True
            )
            grid_layout = GridLayout(
                cols=2,
                size_hint_y=None,
                height=dp(300),
                padding=dp(5),
                spacing=dp(5)
            )

            keys_to_display = ['firstName', 'lastName', 'motherName', 'fatherName', 'address', 'phoneNo', 'email', 'description']
            for key in keys_to_display:
                value = employee_data.get(key, 'N/A')
                if key == 'createdAt' and 'T' in value:
                    try:
                        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
                    except ValueError as e:
                        print(f"Error parsing date: {e}")
                        value = "Unknown"
                
                label_key = MDLabel(
                    text=key.replace('_', ' ').title() + ':',
                    size_hint_y=None,
                    height=dp(40),
                    halign='center',
                    valign='middle',
                    font_style='Subtitle1',
                    color=(0, 0, 0, 1)  
                )
                
                label_value = MDLabel(
                    text=str(value),
                    size_hint_y=None,
                    height=dp(40),
                    halign='center',
                    valign='middle',
                    font_style='Subtitle1',  
                    color=(0.3, 0.3, 0.3, 1)  
                )

                grid_layout.add_widget(label_key)
                grid_layout.add_widget(label_value)

            card.add_widget(scroll_view)
            scroll_view.add_widget(grid_layout)


            #card.add_widget(empty_widget)
            self.personal_info_card = card
            scroll_container.add_widget(card)
        else:
            success_screen.ids.scroll_container.clear_widgets()
            success_screen.ids.scroll_container.add_widget(self.personal_info_card)



if __name__ == '__main__':
    MainApp().run()

"""            empty_widget = Widget(
                size_hint_y=None,
                height=dp(50)
            )"""