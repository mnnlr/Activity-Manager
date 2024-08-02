import requests

class Profile:
    def __init__(self, user_data):
        self.user_data = user_data
        self.profile_data = {}

    def _get_attendance_data(self):
        url = f"https://mnnlr-backend.onrender.com/api/v1/performance/attendance/{self.user_data['user_id']}"
        headers = {'Authorization': f"Bearer {self.user_data['access_token']}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            print(response.json())
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
            return None

    def _get_employee_data(self, employee_id):
        url = f"https://mnnlr-backend.onrender.com/api/v1/employee/{employee_id}"
        headers = {'Authorization': f"Bearer {self.user_data['access_token']}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
            return None

    def getProfileData(self):
        attendance_data = self._get_attendance_data()
        
        if not attendance_data:
            print("Failed to fetch attendance data. Redirecting to login page.")
            return None
        data = attendance_data.get('Data')
        employee_id = data.get('employeeDocId')
        
        if employee_id:
            employee_data = self._get_employee_data(employee_id)
            
            if not employee_data:
                print("Failed to fetch employee data. Redirecting to login page.")
                return None
            
            self.profile_data['attendance_data'] = attendance_data
            self.profile_data['employee_data'] = employee_data
        
        return self.profile_data


