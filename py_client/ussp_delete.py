import requests

product_id = input('What is the product id you want to use?\n')
try:
    product_id = int(product_id)
except:
    print(f'{product_id} is not valid')

if product_id:

    endpoint = f'http://localhost:8000/api/sets/ussp/{product_id}/delete/'

    get_response = requests.delete(endpoint)
    # print(get_response.text)

    print(get_response.status_code)