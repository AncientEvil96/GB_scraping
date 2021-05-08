import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import quote
from copy import deepcopy
from instagram_parser.ista_pars.items import IstaParsItem
from scrapy.loader import ItemLoader


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    def __init__(self, search: list):
        super().__init__()
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'

        # self.username = "dedparser"
        # self.enc_password = "#PWD_INSTAGRAM_BROWSER:10:1619802040:Ac5QAK8dlogyKwvTpn7zJ3IqPNfATwPOfvMuadjURSIzveImb" \
        #                     "SJC6Of7A/60KCVGzrSyaeMD1YtLJSvLmumLoxeal15ZWMjQrgazyFgfOZGAw0mkHBqXE47ta7HSUNMwCo35u/E" \
        #                     "lfxoDedfZu9RzJxRO"

        self.search_list = search
        # self.posts_hash = '32b14723a678bd4628d70c1f877b94c9'
        self.following_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'
        self.followers_hash = '5aefa9893005572d237da5068082d8d5'
        self.graphql_url = "graphql/query/?"

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method='POST',
            callback=self.user_login,
            formdata={
                'username': self.username,
                'enc_password': self.enc_password
            },
            headers={
                'x-csrftoken': csrf_token
            }
        )

    def user_login(self, response: HtmlResponse):
        data = response.json()
        if data['authenticated']:
            for user in self.search_list:
                url = f'{self.start_urls[0]}{user}'
                yield response.follow(
                    url,
                    callback=self.user_data_parse,
                    cb_kwargs={
                        'username': user,
                        'user_url': url
                    }
                )
                print()

    def user_data_parse(self, response: HtmlResponse, username, user_url):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'include_reel': True,
                     'fetch_mutual': False,
                     'first': 12
                     }
        str_variables = self.make_str_variables(variables)

        yield response.follow(
            f'{self.start_urls[0]}{self.graphql_url}query_hash={self.following_hash}&variables={str_variables}',
            callback=self.user_following_parse,
            cb_kwargs={
                'user_id': user_id,
                'variables': deepcopy(variables),
                'username': username,
                'user_url': user_url
            }
        )

        yield response.follow(
            f'{self.start_urls[0]}{self.graphql_url}query_hash={self.followers_hash}&variables={str_variables}',
            callback=self.user_followers_parse,
            cb_kwargs={
                'user_id': user_id,
                'variables': deepcopy(variables),
                'username': username,
                'user_url': user_url
            }
        )

    def make_str_variables(self, variables):
        str_variables = quote(
            str(variables).replace(" ", "").replace("'", '"').replace('True', 'true').replace('False', 'false')
        )
        return str_variables

    def user_following_parse(self, response: HtmlResponse, user_id, variables, username, user_url):
        data = response.json()
        edge_follow = data['data']['user']['edge_follow']

        item = IstaParsItem()
        loader = ItemLoader(item=item, response=response)
        loader.add_value('id', user_id)
        loader.add_value('name', username)
        loader.add_value('url', user_url)
        loader.add_value('user_data', self.get_dict())
        loader.add_value('data_type', 'following')
        loader.add_value('info', edge_follow['edges'])
        yield loader.load_item()

        page_info = edge_follow['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            str_variables = self.make_str_variables(variables)

            yield response.follow(
                f'{self.start_urls[0]}{self.graphql_url}query_hash={self.following_hash}&variables={str_variables}',
                callback=self.user_following_parse,
                cb_kwargs={
                    "user_id": user_id,
                    "variables": deepcopy(variables),
                }
            )

    def get_dict(self):
        return {'following': [], 'followers': []}

    def user_followers_parse(self, response: HtmlResponse, user_id, variables, username, user_url):
        data = response.json()
        edge_followed_by = data['data']['user']['edge_followed_by']

        item = IstaParsItem()
        loader = ItemLoader(item=item, response=response)
        loader.add_value('id', user_id)
        loader.add_value('name', username)
        loader.add_value('url', user_url)
        loader.add_value('user_data', self.get_dict())
        loader.add_value('data_type', 'followers')
        loader.add_value('info', edge_followed_by['edges'])
        yield loader.load_item()

        page_info = edge_followed_by['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            str_variables = self.make_str_variables(variables)

            yield response.follow(
                f'{self.start_urls[0]}{self.graphql_url}query_hash={self.followers_hash}&variables={str_variables}',
                callback=self.user_followers_parse,
                cb_kwargs={
                    "user_id": user_id,
                    "variables": deepcopy(variables),
                }
            )

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
