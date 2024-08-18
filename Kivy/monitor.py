from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import ScreenManager
from login_screen import LoginScreen
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from success_screen import SuccessScreen
from logout_action import perform_logout  
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
import sys
from kivy.core.window import Window
from kivy.resources import resource_add_path, resource_find
from kivy.config import Config




Config.set('kivy','window_icon','C:\\Users\\ootal\\OneDrive\\Desktop\\Activity-Manager\\Kivy\\logo.png')
Config.set('graphics', 'multisamples', '0')  
Config.set('graphics', 'gl_backend', 'angle_sdl2')  

if getattr(sys, 'frozen', False):  
    resource_add_path(sys._MEIPASS)


Window.size = (1080, 768)  

class ProfileCard(MDCard):
    name = StringProperty("")
    email = StringProperty("")
    phone_number = StringProperty("")
    address = StringProperty("")


class EmployeeInfo(AnchorLayout):
    employeeid = StringProperty("N/A")
    joined = StringProperty("N/A")
    designation = StringProperty("N/A")
    designationlevel = StringProperty("N/A")
    shift = StringProperty("N/A")

    def __init__(self, employeeid="N/A", joined="N/A", designation="N/A", designationlevel="N/A", shift="N/A", **kwargs):
        super().__init__(**kwargs)
        self.employeeid = employeeid
        self.joined = joined 
        self.designation = designation 
        self.designationlevel = designationlevel
        self.shift = shift 

class PersonalInfo(AnchorLayout):
    firstname = StringProperty("N/A")
    lastname = StringProperty("N/A")
    fathername = StringProperty("N/A")
    mothername = StringProperty("N/A")
    address = StringProperty("N/A")
    phone = StringProperty("N/A")
    email = StringProperty("N/A")
    description = StringProperty("N/A")

    def __init__(self, firstname="N/A", lastname="N/A", mothername="N/A", fathername="N/A", address="N/A", email="N/A", phone="N/A", description="N/A", **kwargs):
        super().__init__(**kwargs)
        self.firstname = firstname 
        self.lastname = lastname
        self.mothername = mothername 
        self.fathername = fathername 
        self.address = address 
        self.phone = phone 
        self.email = email 
        self.description = description

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.icon = 'logo.png'
        Builder.load_file(resource_find('login.kv'))
        Builder.load_file(resource_find('sample.kv'))
        self.screen_manager = ScreenManager()
        
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(SuccessScreen(name='success', perform_logout=perform_logout, screen_manager=self.screen_manager))
        return self.screen_manager

    def login(self):
        
        login_screen = self.screen_manager.get_screen('login')
        username = login_screen.ids.user.text
        password = login_screen.ids.password.text
        
        login_screen.userlogin(username, password,self.display_table)

    def logout(self):
        
        access_token = self.screen_manager.get_screen('success').user_data.get('access_token')
        cookie = self.screen_manager.get_screen('login').cookies


        def on_success():
            self.show_message("Logout", "Logout Successful")
            success_screen = self.screen_manager.get_screen('success')

            if hasattr(self, 'attendance_table') or hasattr(self, 'personal_info_card') or hasattr(self, 'employee_info_card'):
                success_screen.ids.scroll_container.clear_widgets()

                if hasattr(self, 'attendance_table'):
                    del self.attendance_table

                if hasattr(self, 'personal_info_card'):
                    del self.personal_info_card

                if hasattr(self, 'employee_info_card'):
                    del self.employee_info_card

            self.screen_manager.get_screen('success').user_data.clear()
            self.screen_manager.get_screen('login').user_data.clear()

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
            print("table printing for the first time")
            scroll_container = success_screen.ids.scroll_container
            scroll_container.clear_widgets()
            login_screen = self.screen_manager.get_screen('login')
            attendance_data = login_screen.get_attendance_data()

            if not attendance_data or not attendance_data.get('success'):
                return

            data = attendance_data.get('Data', {})
            time_tracking = data.get('timeTracking', [])

            formatted_data = [
                (str(index + 1), entry.get('timeIn', 'N/A'),
                 entry.get('timeOut','N/A') if index != 0 else 'Working Now'
                 , entry.get('duration', 'N/A'))
                for index, entry in enumerate(time_tracking)
            ]
            print(formatted_data)
            layout = AnchorLayout(
                size_hint = (1,1),
                anchor_x = 'center',
                anchor_y = 'top',

            )

            table = MDDataTable(
                size_hint_x = 1,
                size_hint_y = 1,
                rows_num=len(time_tracking),
                column_data=[
                    ("Login Count", dp(60)),
                    ("Login Time", dp(60)),
                    ("Logout Time",dp(60)),
                    ("Duration", dp(60))
                ],
                row_data=formatted_data,
                pos_hint={"center_x":.5,"center_y":.5},
            )
            
            layout.add_widget(table)
            self.attendance_table = layout
            scroll_container.add_widget(layout)
        else:
            print("rendering already printed")
            success_screen.ids.scroll_container.clear_widgets()
            success_screen.ids.scroll_container.add_widget(self.attendance_table)
    def display_personalinfo(self):
        success_screen = self.screen_manager.get_screen('success')
        success_screen.ids.widget.text = "Personal Information"
        

        if not hasattr(self, 'personal_info_card'):
            scroll_container = success_screen.ids.scroll_container
            scroll_container.clear_widgets()
            
    
            login_screen = self.screen_manager.get_screen('login')
            employee_data = login_screen.get_employee_data()

            
            personal_info_card = PersonalInfo(
                firstname=employee_data.get('firstName', 'N/A'),
                lastname=employee_data.get('lastName', 'N/A'),
                mothername=employee_data.get('motherName', 'N/A'),
                fathername=employee_data.get('fatherName', 'N/A'),
                address=employee_data.get('address', 'N/A'),
                phone=str(employee_data.get('phoneNo', 'N/A')),
                email=employee_data.get('email', 'N/A'),
                description=employee_data.get('description', 'N/A'),
                pos_hint={"center_x":.5,"center_y":.5},
                anchor_x = 'center',
                anchor_y = 'center',
            )

            
            scroll_container.add_widget(personal_info_card)

           
            self.personal_info_card = personal_info_card
        else:
            success_screen.ids.scroll_container.clear_widgets()
            success_screen.ids.scroll_container.add_widget(self.personal_info_card)
    def display_employeeinfo(self):
        success_screen = self.screen_manager.get_screen('success')
        success_screen.ids.widget.text = "Employee Info"
    
        if not hasattr(self, 'employee_info_card'):
            scroll_container = success_screen.ids.scroll_container
            scroll_container.clear_widgets()
            
            login_screen = self.screen_manager.get_screen('login')
            employee_data = login_screen.get_employee_data()

            
            employee_info_card = EmployeeInfo(
                employeeid=employee_data.get('employeeId', 'N/A'),
                joined = employee_data.get('createdAt', 'N/A').split('T')[0],
                designation=employee_data.get('designation', 'N/A'),
                designationlevel=employee_data.get('designationLevel', 'N/A'),
                shift=employee_data.get('Shift', 'N/A'),
                pos_hint={"center_x":.5,"center_y":.5},
                anchor_x = 'center',
                anchor_y = 'center',
            )

           
            scroll_container.add_widget(employee_info_card)
            self.employee_info_card = employee_info_card
        else:
            success_screen.ids.scroll_container.clear_widgets()
            success_screen.ids.scroll_container.add_widget(self.employee_info_card)




if __name__ == '__main__':
    MainApp().run()

