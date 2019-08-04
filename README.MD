# mi application

import requests

url = 'http://127.0.0.1:8000/api/auth/login/'

data = {
  'username': 'lorena',
  'password': 'lorena',
}

response = requests.post(url, json=data)

res_json = response.json()
token = res_json.get('token')


url_insumos = 'http://127.0.0.1:8000/api/insumos/'

headers = {
  'Authorization': 'Token ' + token
}

response = requests.get(url_insumos, headers=headers)


url_insumos = 'http://127.0.0.1:8000/api/insumos/'

# jwt Bearer not Token
headers = {
   'Authorization': 'Bearer ' + token
 }

response = requests.get(url_insumos, headers=headers)
