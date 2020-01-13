import requests

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Accept': 'application/vnd.github.v3+json',
}

api_url = 'https://api.github.com/users/bolshakoVofficial/repos'

response = requests.get(api_url, headers=headers)
reps_json = response.text

f = open('reps.json', 'w')
f.write(str(reps_json))

print(1)
