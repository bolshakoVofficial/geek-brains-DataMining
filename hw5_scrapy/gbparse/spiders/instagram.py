# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import json
from urllib.parse import urlencode
from copy import deepcopy
import re
from hw5_scrapy.gbparse.items import FollowersItem
from hw5_scrapy.gbparse.items import FollowingItem

HASHES = {
    'followers': 'c76146de99bb02f6415203be841dd25a',
    'following': 'd04b0a864b4b54837c0d870b0e77e076',
    'media': '58b6785bea111c67129decbe6a448951',
    'media_comments': '97b41c52301f77ce508f55e66d17620e',
    'likes': 'd5d763b1e2acf209d62d22d184488e57',
    'tags': '174a5243287c5f3a7de741089750ab3b',
}


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = ''
    insta_pass = ''
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'youre.goddamn.right'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    def parse(self, response: HtmlResponse):
        token = response.xpath('//script[@type="text/javascript"]/text()').extract()[3]
        csrf_token = token.split('":"')[1].split('","')[0]

        yield scrapy.FormRequest(
            self.insta_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'password': self.insta_pass},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.userdata_parse,
                cb_kwargs={'username': self.parse_user}
            )
        else:
            print('Not authenticated!')

    def userdata_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)

        variables = {
            'id': user_id,
            "include_reel": True,
            "include_logged_out_extras": False,
            "first": 100,
        }

        url_followers = f'{self.graphql_url}query_hash={HASHES["followers"]}&{urlencode(variables)}'

        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)
                       }

        )

        url_following = f'{self.graphql_url}query_hash={HASHES["following"]}&{urlencode(variables)}'

        yield response.follow(
            url_following,
            callback=self.user_following_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)
                       }
        )

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.body)
        j_page_info = j_data["data"]["user"]["edge_followed_by"]["page_info"]
        j_followed = j_data["data"]["user"]["edge_followed_by"]["edges"]

        if j_page_info["has_next_page"]:
            variables["after"] = j_page_info["end_cursor"]

            url_followers = f'{self.graphql_url}query_hash={HASHES["followers"]}&{urlencode(variables)}'

            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)
                           }
            )

        for follower in j_followed:
            item = FollowersItem(
                user_name=username,
                user_id=user_id,
                follower_name=follower["node"]["username"],
                follower_id=follower["node"]["id"],
                data=follower["node"],
            )
            yield item

    def user_following_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.body)
        j_page_info = j_data["data"]["user"]["edge_follow"]["page_info"]
        j_following = j_data["data"]["user"]["edge_follow"]["edges"]

        if j_page_info["has_next_page"]:
            variables["after"] = j_page_info["end_cursor"]

            url_following = f'{self.graphql_url}query_hash={HASHES["following"]}&{urlencode(variables)}'

            yield response.follow(
                url_following,
                callback=self.user_following_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)
                           }
            )

        for follow in j_following:
            item = FollowingItem(
                user_name=username,
                user_id=user_id,
                following_name=follow["node"]["username"],
                following_id=follow["node"]["id"],
                data=follow["node"],
            )

            yield item

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
