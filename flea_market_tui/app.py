import sys
from pathlib import Path
from typing import Any, Tuple, Callable

import requests as requests
from valid8 import validate, ValidationError

from flea_market_tui.domain import FleaMarket, Username, Password, Email, Item, Name, Description, Price, Brand, \
    Condition, Category
from flea_market_tui.menu import Menu, MenuDescription, Entry

api_address = 'http://localhost:8000/api/v1/'

class App:
    __logged = False
    __key = None
    __id_dictionary = []

    def __init__(self):
        self.__login_menu = self.init_login_menu()
        self.__home_menu = self.__init_home_menu()
        self.__fleamarket = FleaMarket()

    def init_login_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('SIGN-IN'), auto_select=lambda: print('Welcome!')) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.__login())) \
            .with_entry(Entry.create('2', 'Register', on_selected=lambda: self.__register())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Exited!'), is_exit=True)) \
            .build()

    def __init_home_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('FLEA-MARKET'), auto_select=lambda: self.__print_items()) \
            .with_entry(Entry.create('1', 'Add Item', on_selected=lambda: self.__add_item())) \
            .with_entry(Entry.create('2', 'Remove Item', on_selected=lambda: self.__remove_item())) \
            .with_entry(Entry.create('3', 'Sort by Price', on_selected=lambda: self.__sort_by_price())) \
            .with_entry(Entry.create('4', 'Sort by Condition', on_selected=lambda: self.__sort_by_condition())) \
            .with_entry(Entry.create('5', 'Sort by Brand', on_selected=lambda: self.__sort_by_brand())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Exited!'), is_exit=True)) \
            .build()

    def __login(self) -> bool:
        username = self.__read("Username", Username)
        password = self.__read("Password", Password)

        res = requests.post(url=f'{api_address}auth/login/', data={'username': username, 'password': password})

        if res.status_code != 200:
            print('User does not exist :( Please retry!')
            return False
        self.__key = res.json()['key']
        return True

    def __register(self) -> None:
        username = self.__read("Username", Username)
        email = self.__read("Email", Email)
        password = self.__read("Password", Password)

        res = requests.post(url=f'{api_address}auth/registration/', data={'username': username, 'email': email, 'password1': password, 'password2': password})

        if res.status_code == 400:
            print('User already exists :( Please retry!')

    def __print_items(self) -> None:
        print_separator = lambda: print('-' * 200)

        print_separator()

        fmt = '%-3s %-30s %-30s %-30s %-30s %-30s %-50s'
        print(fmt % ('#', 'NAME', 'DESCRIPTION', 'CONDITION', 'BRAND', 'PRICE', 'CATEGORY'))

        print_separator()

        print(self.__fleamarket.items())

        for index in range(self.__fleamarket.items()):
            item = self.__fleamarket.item(index)
            print(fmt % (index + 1, item.name, item.description, item.condition, item.brand, item.price, item.category))

        print_separator()

    def __add_item(self) -> None:
        item = Item(*self.__read_item())
        try:
            self.__fleamarket.add_item(item)
            self.__save(item)
            print('Item added!')
        except ValueError:
            print('Item already exist in the list!')

    def __remove_item(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__fleamarket.items())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return

        self.__delete(self.__fleamarket.item(index - 1))
        self.__fleamarket.remove_item(index - 1)
        print('Item removed!')

    def __sort_by_price(self) -> None:
        self.__fleamarket.sort_by_price()

    def __sort_by_condition(self) -> None:
        self.__fleamarket.sort_by_condition()

    def __sort_by_brand(self) -> None:
        self.__fleamarket.sort_by_brand()

    def __run(self) -> None:
        while not self.__login_menu.run() == (True, False):  # So continue while user is not exited and is logged!
            try:
                self.__fetch()
            except ValueError as e:
                print('Continuing with an empty list of items...')
            except RuntimeError:
                print('Failed to connect to the server!')
                return

            self.__home_menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print(e)
            print('Panic error!', file=sys.stderr)

    def __fetch(self) -> None:
        res = requests.get(url=f'{api_address}item/', headers={'Authorization': f'Token {self.__key}'})

        if res.status_code != 200:
            raise RuntimeError()

        items = res.json()
        for item in items:
            validate('row length', item, length=7)

            item_id = int(item['id'])
            name = Name(str(item['name']))
            description = Description(str(item['description']))
            condition = Condition(str(item['condition']))
            brand = Brand(str(item['brand']))
            price = Price.create(int(int(item['price']) / 100), int(item['price']) % 100)
            category = Category(str(item['category']))

            self.__id_dictionary.append([item_id, name.value, brand.value])

            self.__fleamarket.add_item(Item(name, description, condition, brand, price, category))

            print(item)

    def __save(self, item: Any) -> None:
        req = requests.post(url=f'{api_address}item/add/',
                            headers={'Authorization': f'Token {self.__key}'},
                            data={'name': item.name.value, 'description': item.description.value,
                                  'condition': item.condition.value, 'brand': item.brand.value,
                                  'price': item.price.value_in_cents, 'category': item.category})

        self.__id_dictionary.append([req.json()['id'], item.name.value, item.brand.value])

    def __update(self, item: Any) -> None:
        for i in range(len(self.__id_dictionary)):
            if (item.name.value, item.brand.value) == (self.__id_dictionary[i][1], self.__id_dictionary[i][2]):
                requests.patch(url=f'{api_address}item/edit/{self.__id_dictionary[i][0]}',
                               headers={'Authorization': f'Token {self.__key}'},
                               data={'name': item.name.value, 'description': item.description.value,
                                  'condition': item.condition.value, 'brand': item.brand.value,
                                  'price': item.price.value_in_cents, 'category': item.category})
                break

    def __delete(self, item: Any) -> None:
        index = None
        for i in range(len(self.__id_dictionary)):
            if (item.name.value, item.manufacturer.value) == (self.__id_dictionary[i][1], self.__id_dictionary[i][2]):
                requests.delete(url=f'{api_address}item/edit/{self.__id_dictionary[i][0]}',
                                headers={'Authorization': f'Token {self.__key}'})
                index = i
                break
        self.__id_dictionary.pop(index)

    def __read_item(self) -> Tuple[Name, Description, Condition, Brand, Price, Category]:
        item = self.__read('Name', Name)
        description = self.__read('Description', Description)
        condition = self.__read('Condition', Condition)
        brand = self.__read('Brand', Brand)
        price = self.__read('Price', Price.parse)
        category = self.__read('Category', Category)

        return item, description, condition, brand, price, category

    # COSA FA? O.O
    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                if prompt != 'Password':
                    line = input(f'{prompt}: ')
                else:
                    line = input(f'{prompt}: ')
                    # line = getpass(f'{prompt}: ')

                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)


#  _____________MAIN_____________
def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)



