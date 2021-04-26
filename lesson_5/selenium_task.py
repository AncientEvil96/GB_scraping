# Написать программу, которая собирает посты из группы https://vk.com/tokyofashion
# Будьте внимательны к сайту!
# Делайте задержки, не делайте частых запросов!
#
# 1) В программе должен быть ввод, который передается в поисковую строку по постам группы
# 2) Соберите данные постов:
# - Дата поста
# - Текст поста
# - Ссылка на пост(полная)
# - Ссылки на изображения(если они есть)
# - Количество лайков, "поделиться" и просмотров поста
# 3) Сохраните собранные данные в MongoDB
# 4) Скролльте страницу, чтобы получить больше постов(хотя бы 2-3 раза)
# 5) (Дополнительно, необязательно) Придумайте как можно скроллить "до конца" до тех пор пока посты не
# перестанут добавляться
#
# Чем пользоваться?
# Selenium, можно пользоваться lxml, BeautifulSoup
#
# Советы
# Пример изменения Selenium через Options - https://gb.ru/lessons/124838#!#comment-723755
# Посмотрите комментарий по задаче - https://gb.ru/lessons/124838#!#comment-723755
#
# Если какая-то из ссылок не открывается - напишите в ЛС, исправим

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from mongo import MongoCollectionProcessor
from pymongo import MongoClient
import logging


class SeleniumDriver:
    def __init__(self):
        logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
        self._driver_path = './chromedriver'
        self.posts = []
        self.info_list = []
        self.full_posts = []
        self.driver_s = None

    def connect_driver(self):
        self.driver_s = webdriver.Chrome(self._driver_path)

    def get_vk_post(self, url):
        self.driver_s.get(url)
        self.check_captche()
        time.sleep(1)
        search = self.driver_s.find_element_by_xpath('//a[contains(@class,"tab_search")]')
        url_search = search.get_attribute('href')
        self.driver_s.get(url_search)
        search = self.driver_s.find_element_by_xpath('//input[@id="wall_search"]')
        search.send_keys('отличная' + Keys.ENTER)
        time.sleep(1)
        url_search = self.driver_s.current_url
        self.driver_s.get(url_search)

    def get_all_post(self):
        old_len_posts = 0
        while True:
            self.full_posts = self.driver_s.find_elements_by_xpath('//div[@class="_post_content"]')
            actions = ActionChains(self.driver_s)
            actions.move_to_element(self.full_posts[-1])
            actions.perform()
            time.sleep(1)

            if len(self.full_posts) == old_len_posts:
                break
            else:
                old_len_posts = len(self.full_posts)

    def get_info(self):
        for post in self.full_posts:
            info = {}
            open_post = post.find_element_by_class_name('wall_post_text')
            try:
                info['text'] = open_post.text
                open_post.click()
                time.sleep(1)
                info['href'] = self.driver_s.current_url
                list_img = self.driver_s.find_elements_by_xpath(
                    '//div[@class="wl_post_body_wrap"]//a[contains(@class,"image_cover")]')
                info['img'] = [i.get_attribute('style').split(';')[2][24:-2] for i in list_img]
                info['date'] = self.driver_s.find_element_by_xpath(
                    '//div[@class="post_header "]//div[@class="post_date"]/a[@class="post_link"]').text
                info['like'] = self.driver_s.find_element_by_xpath(
                    '//div[contains(@class,"post_actions_wrap")]//div[@class="like_cont "]'
                    '//a[contains(@class,"_like")]').get_attribute(
                    'data-count')
                info['reposts'] = self.driver_s.find_element_by_xpath(
                    '//div[contains(@class,"post_actions_wrap")]//div[@class="like_cont "]'
                    '//a[contains(@class,"_share")]').get_attribute(
                    'data-count')
                info['views'] = self.driver_s.find_element_by_xpath(
                    '//div[contains(@class,"post_actions_wrap")]//div[@class="like_cont "]'
                    '//div[contains(@class,"_views")]').text
                time.sleep(2)
                self.driver_s.back()
                self.info_list.append(info)
            except Exception:
                logging.info('no loading')

        time.sleep(1)
        self.driver_s.quit()

    def check_captche(self):
        try:
            time.sleep(1)
            tag_to_captcha = self.driver_s.find_element_by_xpath('//button[contains(text(),"Cancel")]')
            tag_to_captcha.click()
        except Exception as err:
            logging.info('no captche')


if __name__ == '__main__':
    # logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
    # driver_path = './chromedriver'
    # driver = webdriver.Chrome(driver_path)
    url = 'https://vk.com/tokyofashion'
    # driver.get(url)
    #
    # # вдруг капча
    # try:
    #     time.sleep(1)
    #     tag_to_captcha = driver.find_element_by_xpath('//button[contains(text(),"Cancel")]')
    #     tag_to_captcha.click()
    # except Exception as err:
    #     logging.info('no captche')
    #
    # time.sleep(1)
    # search = driver.find_element_by_xpath('//a[contains(@class,"tab_search")]')
    # url_search = search.get_attribute('href')
    # driver.get(url_search)
    # search = driver.find_element_by_xpath('//input[@id="wall_search"]')
    # search.send_keys('отличная' + Keys.ENTER)
    # time.sleep(1)
    # url_search = driver.current_url
    # driver.get(url_search)
    #
    # old_len_posts = 0
    # while True:
    #     full_posts = driver.find_elements_by_xpath('//div[@class="_post_content"]')
    #     actions = ActionChains(driver)
    #     actions.move_to_element(full_posts[-1])
    #     actions.perform()
    #     time.sleep(1)
    #
    #     if len(full_posts) == old_len_posts:
    #         break
    #     else:
    #         old_len_posts = len(full_posts)
    #
    # info_list = []
    # for post in full_posts:
    #     info = {}
    #     open_post = post.find_element_by_class_name('wall_post_text')
    #     try:
    #         info['text'] = open_post.text
    #         open_post.click()
    #         time.sleep(1)
    #         info['href'] = driver.current_url
    #         list_img = driver.find_elements_by_xpath(
    #             '//div[@class="wl_post_body_wrap"]//a[contains(@class,"image_cover")]')
    #         info['img'] = [i.get_attribute('style').split(';')[2][24:-2] for i in list_img]
    #         info['date'] = driver.find_element_by_xpath(
    #             '//div[@class="post_header "]//div[@class="post_date"]/a[@class="post_link"]').text
    #         # footer = driver.find_element_by_xpath('//div[contains(@class,"post_actions_wrap")]//div[@class="like_cont "]')
    #         # info['like'] = footer.find_element_by_xpath('//a[contains(@class,"_like")]').text
    #         # info['reposts'] = footer.find_element_by_xpath('//a[contains(@class,"_share")]').text
    #         # info['views'] = footer.find_element_by_xpath('//div[contains(@class,"_views")]').text
    #         info['like'] = driver.find_element_by_xpath(
    #             '//div[contains(@class,"post_actions_wrap")]//div[@class="like_cont "]//a[contains(@class,"_like")]').get_attribute(
    #             'data-count')
    #         info['reposts'] = driver.find_element_by_xpath(
    #             '//div[contains(@class,"post_actions_wrap")]//div[@class="like_cont "]//a[contains(@class,"_share")]').get_attribute(
    #             'data-count')
    #         info['views'] = driver.find_element_by_xpath(
    #             '//div[contains(@class,"post_actions_wrap")]//div[@class="like_cont "]//div[contains(@class,"_views")]').text
    #         time.sleep(2)
    #         driver.back()
    #         info_list.append(info)
    #     except Exception as err:
    #         logging.info('no loading')
    #
    # time.sleep(1)
    # driver.quit()

    my_sel = SeleniumDriver()
    my_sel.connect_driver()
    my_sel.get_vk_post()
    my_sel.get_all_post()
    my_sel.get_info()

    with MongoClient('localhost:27017') as client:
        db = client['posts']
        collection = db['tokyo_fashion']

        mongo = MongoCollectionProcessor(collection)

        # заполнение данных
        mongo.write_mongo(my_sel.info_list, no_check=False)

        # полная выгрузка
        result = mongo.query_mongo({})
        mongo.result_output(result)
