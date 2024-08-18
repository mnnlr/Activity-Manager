from kivy.uix.screenmanager import Screen
import requests
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from profile_data import Profile
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from extract_cookie import convert_cookies_to_dict
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class LoginScreen(Screen):
    dialog = None
    image = "image.png"
    Dashboard_data = None

    def userlogin(self, username, password, display_table):
        
        
        self.user_data = {}
        try:
            response = requests.post(
                'https://mnnlr-backend.onrender.com/api/v1/login',
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            response_data = response.json()
            self.cookies = convert_cookies_to_dict(response.cookies)
            

            if response.status_code == 200 and response_data.get('success'):
                found_user = response_data.get('foundUser', {})
                self.user_data['access_token'] = found_user.get('accessToken')
                self.user_data['user_id'] = found_user.get('_id')
                success_screen = self.manager.get_screen('success')
                success_screen.user_data = self.user_data
                
                Clock.schedule_once(lambda dt: self.fetch_profile_data(success_screen, display_table))
                
            else:
                self.show_dialog('Login Failed', response_data.get('message', 'Login failed'))

        except requests.RequestException as e:
           
            self.show_dialog('Error', 'An error occurred while logging in. Please try again.')



    def fetch_profile_data(self, success_screen, display_table):
        profile = Profile(self.user_data)
        self.Dashboard_data = profile.getProfileData()
        if self.Dashboard_data:
            attendance_data = self.get_attendance_data()
            employee_data = self.get_employee_data()   
            self.manager.current = 'success'
            self.populate_profile_card(employee_data, attendance_data)
            display_table()
        else:
            self.show_dialog('Error', 'Failed to fetch profile data.')

    def get_attendance_data(self):
        return self.Dashboard_data.get("attendance_data", {})

    def get_employee_data(self):
        return self.Dashboard_data.get("employee_data", {}).get('Data', {})

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

    def populate_profile_card(self, employee_data, attendance_data):
        success_screen = self.manager.get_screen('success')

        data = attendance_data.get('Data', {})
        last_login_data = data.get('timeTracking', [{}])[0]
        last_login_time = last_login_data.get('timeIn', 'N/A')

        profile_card = success_screen.ids.profile_card

        profile_card.ids.name.text = f"{employee_data.get('firstName', '')} {employee_data.get('lastName', '')}"
        profile_card.ids.email.text = f"{employee_data.get('email', '')}"
        profile_card.ids.phone.text = f"{employee_data.get('phoneNo', '')}"
        profile_card.ids.joined.text = f"Joined: {employee_data.get('createdAt', '')[:10]}"
        profile_card.ids.designation.text = f"{employee_data.get('designation', '')}"
        profile_card.ids.avatar.source = employee_data.get('avatar', {}).get('url', 'image.png')
        profile_card.ids.last_login.text = f"Last Login: {str(last_login_time)}"
        profile_card.ids.duration.text = f"Working Hours: {data.get('totalWorkingHours', '')}"
