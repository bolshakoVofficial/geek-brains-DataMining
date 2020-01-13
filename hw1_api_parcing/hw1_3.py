import requests
import time
import codecs

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',

}
params = {'records_per_page': 100, 'page': 1}
url = 'https://5ka.ru/api/v2/categories/'


def get_cat_items(url):
    while True:
        time.sleep(0.5)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break

    items_list = []

    for item in range(len(response.json())):
        items_dict = response.json()[item]
        items_list.append(items_dict['group_name'])

    return items_list


def get_data(url):
    while True:
        time.sleep(0.5)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break

    json_resp = response.json()

    for i in range(len(json_resp)):
        info = {'category_id': json_resp[i]['parent_group_code'],
                'category_name': json_resp[i]['parent_group_name'],
                'items': get_cat_items(url + json_resp[i]['parent_group_code'])}

        filename = str(json_resp[i]['parent_group_name'])
        filename = ''.join(filter(lambda x: x not in ['/', '\n', "\\", '*', '"', '<', '>', '?', ':', '|'], filename))
        f = codecs.open(filename + ".json", "w", "utf-8")
        f.write(str(info))


get_data(url)
