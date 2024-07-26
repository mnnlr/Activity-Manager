



from kivy.uix.screenmanager import Screen
import requests
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class LoginScreen(Screen):
    dialog = None

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
                success_screen = self.manager.get_screen('success')
                success_screen.tokens = tokens

               
                employee_info = response_data.get('employee_info', {})

             
                profile_data = {
                    'first_name': employee_info.get('firstName', 'None'),
                    'last_name': employee_info.get('lastName', 'None'),
                    'fathers_name': employee_info.get('fatherName', 'None'),
                    'mothers_name': employee_info.get('motherName', 'None'),
                    'address': employee_info.get('address', 'None'),
                    'description': employee_info.get('description', 'None'),
                    'phone_number': employee_info.get('phoneNo', 'None'),
                    'email': employee_info.get('email', 'None'),
                    'designation': employee_info.get('designation', 'None'),
                    'designation_level': employee_info.get('designationLevel', 'None'),
                    'employee_id': employee_info.get('employeeId', 'None'),
                    'joined_on': response_data.get('createdAt', 'None') 
                }

                for key, value in profile_data.items():
                    if hasattr(success_screen.ids, key):
                        setattr(success_screen.ids[key], 'text', str(value)) 

                self.manager.current = 'success'
            else:
                self.show_dialog('Login Failed', response_data.get('message', 'Login failed'))
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            self.show_dialog('Error', 'An error occurred while logging in. Please try again.')

    def clear_fields(self):
        self.ids.user.text = ''
        self.ids.password.text = ''

    def show_dialog(self, title, text):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        on_release=self.close_dialog
                    )
                ]
            )
        else:
            self.dialog.title = title
            self.dialog.text = text
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()