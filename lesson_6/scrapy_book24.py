# II вариант
# 1) Создать двух пауков по сбору данных о книгах с сайтов labirint.ru и book24.ru
# 2) Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги
# 3) Собранная информация дожна складываться в базу данных
# (Нужно ли здесь обновление? Нужны ли дубликаты?)

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from mongo import MongoCollectionProcessor
from pymongo import MongoClient
import logging