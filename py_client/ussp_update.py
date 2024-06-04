import requests

endpoint = 'http://localhost:8000/api/sets/ussp/2/update/'

data = {
    'set_title': None,
    'set_code': 'RA01',
    'simulated_price': 99.99
}

get_response = requests.put(endpoint, json=data)
# print(get_response.text)

print(get_response.json())
print(get_response.status_code)