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
from kivy.core.window import Window

Window.size = (1250, 768)  



class ProfileCard(MDCard):
    name = StringProperty("")
    email = StringProperty("")
    phone_number = StringProperty("")
    address = StringProperty("")


class EmployeeInfo(MDCard):
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

class PersonalInfo(MDCard):
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
        Builder.load_file('login.kv')
        Builder.load_file('sample.kv')
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
                size_hint_x = 0.6,
                size_hint_y = 1,
                rows_num=len(time_tracking),
                column_data=[
                    ("Login Count", dp(40)),
                    ("Login Time", dp(40)),
                    ("Logout Time", dp(40)),
                    ("Duration", dp(40))
                ],
                row_data=formatted_data,
                pos_hint={"center_x":.5,"center_y":.5},
				
                
            )
            self.attendance_table = table
            scroll_container.add_widget(table)
        else:
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
				orientation='vertical'
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
                joined=employee_data.get('createdAt', 'N/A'),
                designation=employee_data.get('designation', 'N/A'),
                designationlevel=employee_data.get('designationLevel', 'N/A'),
                shift=employee_data.get('Shift', 'N/A'),
                pos_hint={"center_x":.5,"center_y":.5},
				orientation='vertical'
            )

           
            scroll_container.add_widget(employee_info_card)
            self.employee_info_card = employee_info_card
        else:
            success_screen.ids.scroll_container.clear_widgets()
            success_screen.ids.scroll_container.add_widget(self.employee_info_card)




if __name__ == '__main__':
    MainApp().run()

""" grid_layout.add_widget(empty_widget)
            scroll_view.add_widget(grid_layout)"""