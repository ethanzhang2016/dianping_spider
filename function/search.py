# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
import requests
from faker import Factory
from bs4 import BeautifulSoup

from utils.logger import logger
from utils.config import global_config
from utils.get_file_map import get_map


class Search():
    def __init__(self):
        self.cookie = global_config.getRaw('config', 'Cookie')
        self.ua = global_config.getRaw('config', 'user-agent')
        self.location_id = global_config.getRaw('config', 'location_id')
        self.ua_engine = Factory.create()
        self.word_map = get_map('../files/font_map.json')
        # self.word_map = get_map('./files/font_map.json')

    def get_header(self):
        if self.ua is not None:
            ua = self.ua
        else:
            ua = self.ua_engine.user_agent()
        header = {
            'User-Agent': ua,
            'Cookie': self.cookie
        }
        return header

    def search(self, key_word, need_first_page=True):
        assert isinstance(key_word, str)
        assert key_word != None or key_word.strip() != ''
        logger.info('开始搜索:' + key_word)
        header = self.get_header()
        url = 'http://www.dianping.com/search/keyword/' + str(self.location_id) + '/0_' + str(key_word)
        r = requests.get(url, headers=header)
        text = r.text
        for k, v in self.word_map.items():
            key = str(k).replace('uni', '&#x')
            key = key + ';'
            while key in text:
                text.replace(key, v)
        html = BeautifulSoup(text, 'lxml')
        logger.info('解析完成:' + key_word)
        shop_all_list = html.select('.shop-list')[0].select('li')
        for shop in shop_all_list:
            try:
                image_path = shop.select('.pic')[0].select('a')[0].select('img')[0]['src']
            except:
                image_path = None
            try:
                shop_id = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['data-shopid']
            except:
                shop_id = None
            try:
                detail_url = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['href']
            except:
                detail_url = None
            try:
                name = shop.select('.txt')[0].select('.tit')[0].select('a')[0].text.strip()
            except:
                name = None
            try:
                star_point = \
                    shop.select('.txt')[0].select('.comment')[0].select('.star_icon')[0].select('span')[0]['class'][
                        1].split('_')[1]
            except:
                star_point = None
            try:
                review_number = shop.select('.txt')[0].select('.comment')[0].select('.review-num')[0].text
            except:
                review_number = None
            print()
        print()


if __name__ == '__main__':
    Search().search('大连一方城堡')
