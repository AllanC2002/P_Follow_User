import requests

BASE_URL = "http://localhost:8081"

login_data = {
    "User_mail": "ascorread1",
    "password": "1234"
}

login_response = requests.post("http://localhost:8080/login", json=login_data)
if login_response.status_code != 200:
    print("Error:", login_response.status_code, login_response.json())
    exit()

token = login_response.json()["token"]
print("Token obtenido:", token)

# User to follow
data_follow = {
    "id_following": 15  # id
}

headers = {
    "Authorization": f"Bearer {token}"
}

# Hacer follow
follow_response = requests.post(f"{BASE_URL}/follow", json=data_follow, headers=headers)
print("Follow response:")
print(follow_response.status_code, follow_response.json())
