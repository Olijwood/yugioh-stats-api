import requests

headers = {
    'Authorization': 'Bearer f69a18a572d7c8d25a9f98b3b935c4f758d88d07'
}

endpoint = 'http://localhost:8000/api/sets/ussp/'

data = {
    'set_code': 'PHNI',
    'simulated_price': 60.21
}
print(data)

get_response = requests.post(endpoint, json=data, headers=headers)
# print(get_response.text)

print(get_response.json())
print(get_response.status_code)