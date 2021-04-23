# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.


import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


class GitHub:

    def __init__(self, username, token):
        self._username = username
        self._token = token

    def __str__(self):
        repos_r = requests.get('https://api.github.com/user', auth=(self._username, self._token))
        return repos_r.text

    def get_repos(self):
        repos_r = requests.get('https://api.github.com/user/repos', auth=(self._username, self._token))
        return repos_r.json()

    def save_to_file(self, data):
        with open('data_file.json', 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    username = os.environ.get('username_git', None)
    token = os.getenv('token_git', None)
    print(f' User: {username} connect to  github..')
    gh = GitHub(username, token)
    gh.save_to_file(gh.get_repos())
