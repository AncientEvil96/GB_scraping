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
import mongo
import logging
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    # options = Options()
    # options.add_argument("start-maximized")

    logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
    driver_path = './chromedriver'
    driver = webdriver.Chrome(driver_path)
    url = 'https://vk.com/tokyofashion'
    driver.get(url)

    # вдруг капча
    try:
        time.sleep(1)
        tag_to_captcha = driver.find_element_by_xpath('//button[contains(text(),"Cancel")]')
        tag_to_captcha.click()
    except Exception as err:
        logging.info('no captche')

    time.sleep(1)
    search = driver.find_element_by_xpath('//a[contains(@class,"tab_search")]')
    url_search = search.get_attribute('href')
    # print(url_search)
    # url_search = 'https://vk.com/wall-29341229?offset=0&q=%D0%BE%D1%82%D0%BB%D0%B8%D1%87%D0%BD%D0%B0%D1%8F'
    driver.get(url_search)
    search = driver.find_element_by_xpath('//input[@id="wall_search"]')
    search.send_keys('отличная' + Keys.ENTER)
    time.sleep(2)
    # print(driver.current_url)
    url_search = driver.current_url
    driver.get(url_search)

    # with open('html.html', 'w', encoding='utf-8') as f:
    #     f.write(driver.page_source)

    old_element = None
    for i in range(2):
        article = driver.find_elements_by_xpath('//div[@class="_post_content"]')[-1]
        # print(article)
        actions = ActionChains(driver)
        actions.move_to_element(article)
        actions.perform()
        time.sleep(1)

    # with open('html.html','w', encoding='utf-8') as f:
    #     f.write(driver.page_source)

    # search.click()
    # search.send_keys(Keys.END)


    # info_list = []
    # posts = driver.find_element_by_xpath('//div[@id="page_wall_posts"]//div[@class="_post_content"]')

    time.sleep(10)
    #
    #
    driver.quit()
