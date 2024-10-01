import requests

url = 'http://127.0.0.1:8000/items/'
data = {
  "name": "Laptop",
  "description": "A powerful gaming laptop",
  "price": 900.65,
  "tax": 120.50
}

response = requests.get(url)
print(response.json())
response = requests.post(url, json=data)
print(response.json())

data = {
  "name": "Phone",
  "description": "A powerful Phone",
  "price": 850.65,
  "tax": 78
}

response = requests.post(url, json=data)
print(response.json())

response = requests.get(url)
print(response.json())
