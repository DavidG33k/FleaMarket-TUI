from pathlib import Path


class App:
    __filename = Path(__file__).parent.parent / 'items_dataset.csv'
    __delimiter = '\t'

    def __init__(self):
        self.__first_menu = self.init_first_menu()
        self.__menu = self.__init_shopping_list_menu()
        self.__shoppinglist = ShoppingList()