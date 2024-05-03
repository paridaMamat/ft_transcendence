import requests

endpoint = "" #url
response = requests.get(endpoint, data={'bonjour':'hello'}) #data -> formulaire ! / json
print(response.text)

