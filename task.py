from dadata import Dadata
import sqlite3


def save_users_data(name, token, language):
    with sqlite3.connect("database.db") as sqlite_connection:
        cursor_db = sqlite_connection.cursor()
        cursor_db.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            api_key TEXT NOT NULL,
                            language TEXT NOT NULL 
                             )""")
        insert_data = """INSERT INTO users(name, api_key, language) VALUES(?, ?, ?)"""
        data_tuple = (name, token, language)
        cursor_db.execute(insert_data, data_tuple)


def search_geo(token, language):
    while True:
        user_continue = input('Здесь Вы можете узнать координаты введенного адреса. Продолжить?'
                              ' Введите y / n : ')
        if user_continue == 'y':
            dadata = Dadata(token)
            user_address = input('Введите желаемый адрес: ')
            result = dadata.suggest("address", user_address, language=language)
            punkt = 0
            for i in result:
                punkt += 1
                print(str(punkt) + ': ' + i['value'])
            user_choice = int(input('Введите порядковый номер Вашего объекта: '))
            user_dict = result[user_choice - 1]
            latitude = user_dict['data']['geo_lat']
            longitude = user_dict['data']['geo_lon']
            print('Координаты Вашего объекта: широта: ' + latitude + ' , долгота: ' + longitude)
        elif user_continue == 'n':
            break


if __name__ == "__main__":
    name = input('Введите Ваше имя: ')
    token = input('Введите Ваш API ключ: ')
    choise_language = input('Для ввода запросов и вывода результатов поддерживаются языки: английский/'
                            'русский. Оставить русский язык по умолчанию? Введите y/n : ')
    if choise_language == 'y':
        language = 'ru'
    elif choise_language == 'n':
        language = 'en'

    save_users_data(name, token, language)
    search_geo(token, language)
