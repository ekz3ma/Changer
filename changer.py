import requests
from decouple import config


class BestChange:
    def __init__(self):
        self.API_KEY = config('API_KEY')

    def _parsing_codes(self):
        self.codes = requests.get(f'https://v6.exchangerate-api.com/v6/{self.API_KEY}/codes').json()['supported_codes']
        if self.codes is None:
            print('Данные не загружены, внутренняя ошибка сервера')
            return

    def pagination(self, page: int=1, per_page: int=10):
        BestChange._parsing_codes(self)

        curren = {}

        for code in self.codes:
            curren[code[0]] = [code[1]]

        items = list(curren.items())
        total = len(items)
        start = (page - 1) * per_page
        end = start + per_page

        print(f"\n{'ID':<6} {'Название валюты'}")
        print('-' * 40)

        for curr_name, curr_descript in items[start:end]:
            print(f'[{curr_name}] | {curr_descript[0]}')

        print(f'\nСтраница {page}/{((total - 1) // per_page + 1)}')
        print(f'Всего валют: {total}')


class BestChangeCli:
    def __init__(self):
        self.api = BestChange()

    def select_currency(self):
        while True:
            print('Приветствую вас в валют-обменнике\n1: Посмотреть список валют\n2: Посмотреть обменный курс\n3: Выход')
            user_input = input('> ')

            if user_input == '1':
                page = 1

                while True:
                    self.api.pagination(page=page)
                    print('\n<-[p](назад) [q](выход) [n](далее)-> ')
                    cmd = input('> ').strip().lower()
                    if cmd == 'n':
                        page += 1
                    elif cmd == 'p' and page > 1:
                        page -= 1
                    else:
                        break
            elif user_input == '2':
                try:
                    while True:
                        first_value = str(input('Введите валюту которую хотите менять из списка(в формате кода):\n> ')).upper()
                        second_value = str(input('Введите валюту на которую хотите менять списка(в формате кода):\n> ')).upper()
                        amount = float(input('Количество валюты:\n> '))

                        pair = requests.get(f'https://v6.exchangerate-api.com/v6/{self.api.API_KEY}/pair/{first_value}/{second_value}/{amount}').json()['conversion_result']
                        print(pair)
                        cont = str(input('Продолжить? (Y/N): '))

                        if cont == 'Y' or cont == 'y':
                            continue
                        else:
                            break

                except ValueError as e:
                    print(f'{e}: введите значения кодом валюты из списка, а количество числом (пример - USD RUB 1)\n')
                    continue

                except KeyError as e:
                    print(f'{e}: введите значения из списка')
                    continue

            elif user_input == '3' or user_input == 'q':
                break

if __name__ == '__main__':
    bestchange = BestChangeCli()
    bestchange.select_currency()
