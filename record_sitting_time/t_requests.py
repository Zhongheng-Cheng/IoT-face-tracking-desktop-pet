import requests

url = "http://35.232.170.48:8000/sitting-time"
data = {'start_time': '2021-11-02T12:58:51', 'end_time': '2021-11-02T13:58:51'}

response = requests.post(url=url, params=data)

if response.status_code != 200:
    print(f"Error: {response.content}")
    print("Request URL:", response.request.url)
    print("Request Headers:", response.request.headers)
    print("Request Body:", response.request.body)