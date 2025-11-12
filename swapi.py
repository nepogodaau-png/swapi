import requests
import os
import json


class APIRequester:

    """Базовый класс"""

    def __init__(self, base_url: str):                               
        self.base_url = base_url


    def get(self):

        try:
            response = requests.get(self.base_url, timeout = 10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f'Ошибка при выполнении запроса: {e}')
            return None

    def __repr__(self):
        return f'APIRequester(base_url = "{self.base_url}")'

class SWRequester(APIRequester):

    """Наследник класса"""

    def get_sw_categories(self):

        """ Выполняет запрос к адресу"""

        response = self.get()

        if response:
            try:
                data = response.json()
                return list(data.keys())
            except ValueError:
                print('Ошибка')
                return []
        else:
            return []
    
    def get_sw_info(self, sw_type):

        """Информацию о выбранной категории."""

        url = f'{self.base_url}/{sw_type}/'

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Ошибка при выполнении запроса к {url}: {e}')
            return None

def save_sw_data():

    """Создаем data и сохранение данных"""
    
    sw_api = SWRequester('https://swapi.dev/api/')
    os.makedirs('data', exist_ok = True)

    categories = sw_api.get_sw_categories()
    if not categories:
        print('Задайте категорию')
        return
    
    for categorie in categories:

        data = sw_api.get_sw_info(categorie) # Получаем данные по категории
        if data:
            file_path = os.path.join('data', f'{categorie}.txt')
            with open (file_path, 'w', encoding='utf=8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4) # Сохранение 
        else:
            print(f'Нет данных')


if __name__ == '__main__':

    api = APIRequester('https://swapi.dev/api/')
    response = api.get()

    if response:
        print('Запрос выполнен успешно')
        print('Статус код:', response.status_code)
    else:
        print('Запрос не выполнен.')
    
    sw_api = SWRequester('https://swapi.dev/api/')
    categories = sw_api.get_sw_categories()

    if categories:
        print('Категории:')
        for c in categories:
            print('-', c)
    else:
        print('Не удалось получить категории')

    info = sw_api.get_sw_info('people')
    if info:
        print(info)
    else:
        print('Не удалось получить информацию о категории')
    
    save_sw_data()