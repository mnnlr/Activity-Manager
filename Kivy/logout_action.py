import requests

def perform_logout(cookie, on_success, on_failure):
    try:
        response = requests.post(
            'https://mnnlr-backend.onrender.com/api/v1/logout',
            cookies = cookie,
            headers={'Content-Type': 'application/json'}
            
        )
        print(response)
        if response.status_code == 200:
            on_success() 
        else:
            on_failure(f"Logout Failed: {response.text}")  
    except requests.RequestException as e:
        on_failure(f"An error occurred: {e}")  
