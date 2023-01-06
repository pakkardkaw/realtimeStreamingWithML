import requests
url = 'http://192.168.1.71:8030/'
r = requests.post(url,json={'inputdata':1.8,})
print(r.json())