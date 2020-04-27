import requests

url = 'http://127.0.0.1:8000/users/2'

headers = {'Authorization': 'Token 58be58ca0acb7c38b30da163af32465a5039f418'}

r = requests.get(url, headers=headers)
print(r.text)
