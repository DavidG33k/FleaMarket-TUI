import re
from dataclasses import dataclass, InitVar, field

from typing import Any, Union, List

from typeguard import typechecked

from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Name:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=30, custom=pattern(r'[A-Za-z0-9 \-\_]+'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=200, custom=pattern(r'[A-Za-z0-9\_\-\(\)\.\,\;\&\:\=\è\'\"\! ]*'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Condition:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, is_in={'AS_NEW', 'GOOD_CONDITION', 'ACCEPTABLE_CONDITION'})

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Brand:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=20, custom=pattern(r'^[A-Za-z\_\-\(\)]+'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Price:
    value_in_cents: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 100000000000 - 1
    __parse_pattern = re.compile(r'(?P<euro>\d{0,11})(?:\.(?P<cents>\d{2}))?')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    def __str__(self):
        return f'{self.value_in_cents // 100}.{self.value_in_cents % 100:02}'

    @staticmethod
    def create(euro: int, cents: int = 0) -> 'Price':
        validate('euro', euro, min_value=0, max_value=Price.__max_value // 100)
        validate('cents', cents, min_value=0, max_value=99)
        return Price(euro * 100 + cents, Price.__create_key)

    @staticmethod
    def parse(value: str) -> 'Price':
        m = Price.__parse_pattern.fullmatch(value)
        validate('value', m)
        euro = m.group('euro')
        cents = m.group('cents') if m.group('cents') else 0
        return Price.create(int(euro), int(cents))

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100

    @property
    def euro(self) -> int:
        return self.value_in_cents // 100

    def add(self, other: 'Price') -> 'Price':
        return Price(self.value_in_cents + other.value_in_cents, self.__create_key)


@typechecked
@dataclass(frozen=True, order=True)
class Category:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=30, custom=pattern(r'^[A-Za-z\_\-\(\) ]+'))

    def __str__(self):
        return self.value


#AUTH DATACLASSES
@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=8, max_len=25, custom=pattern(r'[A-Za-z0-9]+[\.]*[A-Za-z]*@[A-Za-z]+\.[a-z]+'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=30, custom=pattern(r'[A-Za-z0-9]+'))

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Password:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=6, max_len=25, custom=pattern(r'[A-Za-z0-9]+'))  # r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!\#*?&])[A-Za-z\d@$!\#*?&]{6,25}$'

    def __str__(self):
        return str(self.value)


# ITEM AND FLEAMARKET DEFINITION
@typechecked
@dataclass(frozen=True, order=True)
class Item:
    name: Name
    description: Description
    condition: Condition
    brand: Brand
    price: Price
    category: Category

@typechecked
@dataclass(frozen=True)
class FleaMarket:
    __items: List[Union[Item]] = field(default_factory=list, init=False)

    def items(self) -> int:
        return len(self.__items)

    def item(self, index: int) -> Item:
        validate('index', index, min_value=0, max_value=self.items() - 1)
        return self.__items[index]

    def add_item(self, item: Item) -> None:
        self.__items.append(item)

    def remove_item(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.items() - 1)
        del self.__items[index]

    def sort_by_price(self) -> None:
        self.__items.sort(key=lambda x: x.price)

    def sort_by_condition(self) -> None:
        self.__items.sort(key=lambda x: x.condition)

    def sort_by_brand(self) -> None:
        self.__items.sort(key=lambda x: x.brand)