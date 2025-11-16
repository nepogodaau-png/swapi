import requests
import os
import json


class APIRequester:
    """Базовый класс"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/") 

    def get(self, endpoint: str = ""):
        """Выполняет GET-запрос к base_url + endpoint"""

        url = f"{self.base_url}/{endpoint.lstrip('/')}"  

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f'Ошибка при выполнении запроса к {url}: {e}')
            return None

    def __repr__(self):
        return f'APIRequester(base_url="{self.base_url}")'


class SWRequester(APIRequester):
    """Наследник класса"""

    def get_sw_categories(self):
        """Получает список категорий SWAPI"""

        response = self.get("")  

        if response:
            try:
                data = response.json()
                return list(data.keys())
            except ValueError:
                print('Ошибка: ответ не JSON')
        return []

    def get_sw_info(self, sw_type):
        """Получает данные выбранной категории"""

        response = self.get(sw_type)  

        if response:
            try:
                return response.json()
            except ValueError:
                print("Ошибка: данные не в формате JSON")
                return None

        return None


def save_sw_data():
    """Создаёт папку data и сохраняет файлы по категориям"""

    sw_api = SWRequester("https://swapi.dev/api")
    os.makedirs("data", exist_ok=True)

    categories = sw_api.get_sw_categories()
    if not categories:
        print("Не удалось получить категории")
        return

    for category in categories:
        print(f"Загружаем: {category}")

        data = sw_api.get_sw_info(category)
        if data:
            file_path = os.path.join("data", f"{category}.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Сохранено в {file_path}")
        else:
            print(f"Нет данных по категории {category}")


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