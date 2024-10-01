import requests

url = 'http://127.0.0.1:8000/users/'
data = {
    "username": "john_doe",
    "email": "john@example.com"
}

response = requests.post(url, json=data)
print(response.json())

response = requests.get('http://127.0.0.1:8000/users/john_doe')
print(response.json())