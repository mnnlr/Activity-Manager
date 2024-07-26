import requests

def perform_logout(access_token, on_success, on_failure):
    try:
        response = requests.post(
            'http://127.0.0.1:5000/logout',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if response.status_code == 200:
            on_success() 
        else:
            on_failure(f"Logout Failed: {response.text}")  
    except requests.RequestException as e:
        on_failure(f"An error occurred: {e}")  
