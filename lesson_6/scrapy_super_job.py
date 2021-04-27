# I вариант
# 1) Доработать паука в имеющемся проекте, чтобы он формировал item по структуре:
# *Наименование вакансии
# *Зарплата от
# *Зарплата до
# *Ссылку на саму вакансию
#
# *Сайт откуда собрана вакансия
# И складывал все записи в БД(любую)
#
# 2) Создать в имеющемся проекте второго паука по сбору вакансий с сайта superjob.
# Паук должен формировать item'ы по аналогичной структуре и складывать данные также в БД
# (Подумайте про обновление! Вам ведь нужна актуальная информация по вакансии)

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from mongo import MongoCollectionProcessor
from pymongo import MongoClient
import logging