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
    driver.get(url_search)
    search = driver.find_element_by_xpath('//input[@id="wall_search"]')
    search.send_keys('отличная' + Keys.ENTER)
    time.sleep(1)
    url_search = driver.current_url
    driver.get(url_search)

    old_len_posts = 0
    while True:
        full_posts = driver.find_elements_by_xpath('//div[@class="_post_content"]')
        actions = ActionChains(driver)
        actions.move_to_element(full_posts[-1])
        actions.perform()
        time.sleep(1)

        break

        if len(full_posts) == old_len_posts:
            break
        else:
            old_len_posts = len(full_posts)

    info_list = []
    for post in full_posts:
        info = {}
        # '//div[@class="wall_post_text"]'
        info['date'] = post.find_element_by_xpath('//div[@class="post_date"]/a').text
        open_post = post.find_element_by_class_name('wall_post_text')
        info['text'] = open_post.text
        info['like'] = open_post.find_element_by_xpath('//a[contains(@class,"_like")]').text
        info['reposts'] = open_post.find_element_by_xpath('//a[contains(@class,"_share")]').text
        info['views'] = open_post.find_element_by_xpath('//div[contains(@class,"_views")]').text
        # try:
        #     list_img = post.find_elements_by_xpath('//div[contains(@class,"_thumbs")]//a[contains(@aria-label,".jpg")]')
        #     info['img'] = [i.get_attribute('style').split(';')[2][24:-2] for i in list_img]
        # except Exception as err:
        #     logging.info('not foto')

        open_post.click()
        time.sleep(1)
        info['href'] = driver.current_url
        list_img = driver.find_elements_by_xpath('//div[@class="wl_post_body_wrap"]//a[contains(@class,"image_cover")]')
        info['img'] = [i.get_attribute('aria-label').replace('фотография Original: ', '') for i in list_img]

        time.sleep(2)
        driver.back()
        info_list.append(info)

    for i in info_list:
        print(i)

    time.sleep(1)
    driver.quit()
