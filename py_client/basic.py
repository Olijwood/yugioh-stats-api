import requests

endpoint = 'http://localhost:8000/api/'

# get_response = requests.post(endpoint, json={'set_title':'Phantom Nightmare',
                                            # 'simulated_price': 48.31})
get_response = requests.post(endpoint, json={'set_title':'Rarity'})
# print(get_response.text)

print(get_response.json())
print(get_response.status_code)