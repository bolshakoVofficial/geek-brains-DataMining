import requests

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Authorization': 'Basic cG9zdG1hbjpwYXNzd29yZA==',
}

url = 'https://postman-echo.com/basic-auth'

response = requests.get(url, headers=headers)

f = open('auth_response.txt', 'w')
f.write(response.text)
print(1)
