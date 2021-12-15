import pytest
from valid8 import ValidationError

from flea_market_tui.domain import FleaMarket, Name, Description, Condition, Brand, Price, Category, Email, Username, Password, Item


def test_condition_value():
    wrong_values = ['', 'no', 'error', '1/1337','javascript:alert(1)']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Condition(value)

    correct_values = ['1', '2', '0']
    for value in correct_values:
        assert Condition(value).value == value


def test_condition_str():
    assert Condition('1').__str__() == '1'


def test_name_value():
    wrong_values = ['', 'TE/ST$', '<script>alert()</script>', 'SPECI$$$ALE', 'A' * 31]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Name(value)

    correct_values = ['Bel Pc', 'GAMEBOY', 'A' * 30]
    for value in correct_values:
        assert Name(value).value == value


def test_name_str():
    assert Name('thinkpad').__str__() == 'thinkpad'


def test_description_value():
    wrong_values = ['TE/ST$ DESCRIZION^$E', '<script>alert()</script>', 'SPECI%ALE', 'A' * 201]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Description(value)

    correct_values = ['BELLA QUESTA DESCRIZIONE', 'GAMEBOY MOLTO BELLO E BEN DESCRITTO', 'A' * 200]
    for value in correct_values:
        assert Description(value).value == value


def test_description_str():
    assert Description('thinkpad buono').__str__() == 'thinkpad buono'


def test_brand_value():
    wrong_values = ['TE/ST$ BRAND^', '<script>alert()</script>', 'SPECI%ALE', 'A' * 21]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Brand(value)

    correct_values = ['GUCCI', 'NIKE', 'A' * 20]
    for value in correct_values:
        assert Brand(value).value == value


def test_brand_str():
    assert Brand('Lenovo').__str__() == 'Lenovo'


def test_category_value():
    wrong_values = ['', 'NOT%GOOD', '<script>alert()</script>', 'SomeError55584', 'NotGOod /1337', 'A' * 31]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Category(value)

    correct_values = ['Case', 'Telefoni', 'Videogiochi', 'A' * 30]
    for value in correct_values:
        assert Category(value).value == value


def test_category_str():
    assert Category('Casa').__str__() == 'Casa'


def test_email_value():
    wrong_values = ['', 'sk@skrt.', '_test@gmail.com', 'asdasd@asd3290.com', '...@outlook.com',
                    'ciccio.pasticcio@', 'ab<c>def@hwejgq.333it', 'ciccio@outlook', 'javascript:alert()',
                    'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Email(value)

    correct_values = ['cicciopasticcio@gmail.com', 'claudiobisio@gmail.com', 'spongebob@outlook.com', 'A' * 15 + '@' + 'gmail.it']
    for value in correct_values:
        assert Email(value).value == value


def test_email_str():
    assert Email('abcd@gmail.com').__str__() == 'abcd@gmail.com'


def test_username_value():
    wrong_values = ['', 'à', '<script>alert()</script>', ' spazio ', '%', 'A' * 31]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Username(value)

    correct_values = ['testcasecarino', 'chiodo2chiodo2', 'riuzaki1997', 'A' * 30]
    for value in correct_values:
        assert Username(value).value == value


def test_username_str():
    assert Username('SpasticMMonkey').__str__() == 'SpasticMMonkey'


def test_password_value():
    wrong_values = ['', '<script>alert()</script>','tantierrori##', 'èàèàèàèàèà', '!?abcd$&/',
                    'A' * 26]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Password(value)

    correct_values = ['bellaPassword123!', 'A'*5+'3'*5+'1'*2+'o'*5+'?'*3, 'B4ST4T3St1?', 'rockyouList--']
    for value in correct_values:
        assert Password(value).value == value


def test_password_str():
    assert Password('Passwd123').__str__() == 'Passwd123'


def test_negative_price():
    with pytest.raises(ValidationError):
        Price.create(-1, 0)


def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)


def test_price_add():
    assert Price.create(24, 99).add(Price.create(0, 1)) == Price.create(25)
    assert Price.create(244, 99).add(Price.create(0, 58)) == Price.create(245,57)


def test_price_no_cents():
    assert Price.create(1, 0) == Price.create(1)

def test_price_parse():
    assert Price.parse('10.20') == Price.create(10, 20)


def test_price_str():
    assert str(Price.create(9, 99)) == '9.99'


def test_price_euro():
    assert Price.create(11, 22).euro == 11


def test_price_cents():
    assert Price.create(11, 22).cents == 22


@pytest.fixture
def items():
    #Name,Description,Condition,Brand, Price Category
    return [
        Item(Name('Airforce'), Description(""),Condition('2'), Brand('Nike'), Price.create(111), Category('Scarpe')),
        Item(Name('ChronoTrigger'), Description(""),Condition('1'), Brand('SquareSoft'), Price.create(6666), Category('Videogiochi')),
        Item(Name('Snes'), Description("Prodotto vintage"), Condition('2'), Brand('Nintendo'), Price.create(3333), Category('Console')),
        Item(Name('Scopa'), Description(""), Condition('0'), Brand('Mastrolindo'), Price.create(363636), Category('Casa e Pulizia')),
        Item(Name('thinkpad'), Description("stolen from the Defcon"),Condition('2'), Brand('Lenovo'),Price.create(636363), Category('Computer')),

    ]


def test_Fleamarket_add_items(items):
    market = FleaMarket()
    index = 0
    for i in items:
        market.add_item(i)
        index += 1
        assert market.items() == index
        assert market.item(index - 1) == i


def test_Fleamarket_remove_item(items):
    market = FleaMarket()
    for i in items:
        market.add_item(i)

    market.remove_item(0)
    market.remove_item(0)
    market.remove_item(0)
    assert market.item(0) == items[3]

    with pytest.raises(ValidationError):
        market.remove_item(market.items())
    with pytest.raises(ValidationError):
        market.remove_item(-1)

    while market.items():
        market.remove_item(0)
    assert market.items() == 0


def test_Fleamarket_sort_by_price(items):
    market = FleaMarket()
    market.add_item(items[0])
    market.add_item(items[1])
    market.sort_by_price()
    assert market.item(0) == items[0]


def test_Fleamarket_sort_by_condition(items):
    market = FleaMarket()
    market.add_item(items[0])
    market.add_item(items[1])
    market.sort_by_condition()
    assert market.item(0) == items[1]


def test_Fleamarket_sort_by_brand(items):
    market = FleaMarket()
    market.add_item(items[0])
    market.add_item(items[1])
    market.sort_by_brand()
    assert market.item(0) == items[0]
