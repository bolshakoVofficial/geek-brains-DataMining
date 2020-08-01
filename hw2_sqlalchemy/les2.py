import requests
from bs4 import BeautifulSoup
from database.db import BlogDb
from database.models import (
    Base,
    BlogPost,
    Writer,
    Tag
)
import time


def find_next_page(soup):
    ul = soup.find('ul', attrs={'class': 'gb__pagination'})
    li = ul.find_all('li', attrs={'class': 'page'})
    next_button = li[-1].find('a', attrs={'rel': 'next'})

    if next_button:
        return li[-1].find('a', attrs={'rel': 'next'})['href']
    else:
        return None


def find_post_url(soup) -> list:
    wrapper = soup.find('div', attrs={'class': 'post-items-wrapper'})
    post_items = wrapper.find_all('div', attrs={'class': 'post-item event'})

    post_url = []

    for i in range(len(post_items)):
        post_url.append(post_items[i].find('a')['href'])

    return post_url


def get_post(url):
    while True:
        time.sleep(0.5)
        response = requests.get(url)
        if response.status_code == 200:
            break

    soup = BeautifulSoup(response.text, 'lxml')

    # todo заголовок статьи
    title = str(soup.find('h1').contents[0])

    # todo дата публикации
    post_date = str(soup.find('time').contents[0])

    # todo url статьи
    post_url = url

    # todo список тегов
    tags = []
    all_tags = soup.find_all('a', attrs={'class': 'small'})
    for i in range(len(all_tags)):
        tags.append(str(all_tags[i].contents[0]))

    # todo имя автора
    author = str(soup.find('div', attrs={'itemprop': 'author'}).contents[0])

    # todo url автора
    author_url = soup.find('div', attrs={'itemprop': 'author'}).parent['href']

    return title, post_date, post_url, tags, author, author_url


def get_data(next_page, db):
    page = 0
    post = 0
    while next_page:
        page += 1
        print(f'Processing {page} page')

        while True:
            time.sleep(0.5)
            response = requests.get(DOMAIN + next_page)
            if response.status_code == 200:
                break

        soup = BeautifulSoup(response.text, 'lxml')

        post_url_list = find_post_url(soup)

        for post_url in post_url_list:
            post += 1
            print(f'Processing post #{post}')

            title, post_date, post_url, tags_list, author, author_url = get_post(DOMAIN + post_url)

            # todo при помощи sqlalchemy сохранить данные в базу.
            tags = check_tags(db, tags_list)
            writer = check_writer(db, author, author_url)
            blogpost = BlogPost(title, post_date, post_url, writer, tags)

            db.session.add(blogpost)
            db.session.commit()

            pass

        next_page = find_next_page(soup)


def check_tags(db, tags_list):
    tags = []
    for tag in tags_list:
        present_tag = db.session.query(Tag).filter_by(name=tag).all()

        if present_tag:
            tags.append(present_tag[0])
        else:
            tags.append(Tag(tag))

    return tags


def check_writer(db, name, url):
    present_writer = db.session.query(Writer).filter_by(url=url).all()

    if present_writer:
        return present_writer[0]
    else:
        return Writer(name, url)


DOMAIN = 'https://geekbrains.ru'
START_PAGE = '/posts'

db_url = 'sqlite:///blogpost.sqlite'
database = BlogDb(db_url)

get_data(START_PAGE, database)

print('Finished')
