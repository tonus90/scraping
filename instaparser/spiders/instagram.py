import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem
from passw import inst_pass

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'tonus88'
    inst_pass = inst_pass
    parse_users = ['frolov.d.d', 'sergio_gonnzaless']
    followers_hash = ['5aefa9893005572d237da5068082d8d5', '3dec7e2c57367ef3da3d987d89f9dbc8']
    graphql_url = 'https://www.instagram.com/graphql/query/'

    def parse(self, response:HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_login,
            formdata={'username':self.inst_login,
                      'enc_password':self.inst_pass,
                      'queryParams':{},
                      'optIntoOneTap':'false'},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_login(self, response:HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username':user}
                )

    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id':user_id,
                     'include_reel':True,
                     'fetch_mutual':True,
                     'first':24}
        for hash in self.followers_hash:
            url_followers = f'{self.graphql_url}?query_hash={hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'variables': deepcopy(variables),
                            'username': username,
                            'user_id': user_id,
                            'hash': hash
                           }
            )


    def user_followers_parse(self, response: HtmlResponse, variables, username, user_id, hash):
        j_data = json.loads(response.text)
        if hash == self.followers_hash[0]:
            page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        elif hash == self.followers_hash[1]:
            page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_followers = f'{self.graphql_url}?query_hash={hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'variables': deepcopy(variables),
                           'username': username,
                           'user_id': user_id,
                           'hash': hash
                           }
            )

        followers=str()
        if hash == self.followers_hash[0]:
            followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        elif hash == self.followers_hash[1]:
            followers = j_data.get('data').get('user').get('edge_follow').get('edges')

        for follower in followers:
            yield InstaparserItem(
                user_id=user_id,
                username=username,
                photo=follower.get('node').get('profile_pic_url'),
                flwr_login_name=follower.get('node').get('username'),
                name=follower.get('node').get('full_name'),
                flwr_id=follower.get('node').get('id'),
                user_data=follower.get('node'),
                hash=hash
            )

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')