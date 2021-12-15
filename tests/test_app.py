import sys
from pathlib import Path
from unittest.mock import patch, mock_open, Mock, call

import pytest

from flea_market_tui.app import App, main
from flea_market_tui.domain import *


@pytest.fixture
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path


def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


def mock_response(status_code, data=[]):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_sign_in_exit(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_input.assert_called()
    mocked_print.assert_any_call('*** SIGN-IN ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Exited!')


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['1', 'udonto', 'sbagliato'])
@patch('builtins.print')
def test_app_sign_in_with_wrong_parameters(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('*** SIGN-IN ***')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_print.assert_any_call('User does not exist :( Please retry!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'Key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})])
@patch('builtins.input', side_effect=['1', 'udonto', 'fazio9898'])
@patch('builtins.print')
def test_app_sign_in_with_correct_parameters(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('*** SIGN-IN ***')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_print.assert_any_call('login successfully')


@patch('requests.post', side_effect=[mock_response_dict(200)])
@patch('builtins.input', side_effect=['2', 'nuovo_username', 'nuova@gmail.com', 'password'])
@patch('builtins.print')
def test_app_registration_user(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_requests_post.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('*** SIGN-IN ***')
    mocked_print.assert_any_call('2:\tRegister')
    mocked_print.assert_any_call('Registration completed!')


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['2', 'pallas', 'pallas@gmail.com', 'antony98'])
@patch('builtins.print')
def test_app_registration_user_already_exist(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('Not Valid new Users!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})])
@patch('requests.get', side_effect=[mock_response_dict(200)])
@patch('builtins.input', side_effect=['1', 'cazzo', 'antony98', '0', '0'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_username(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_print.assert_any_call('*** SIGN-IN ***')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('*** FLEA-MARKET ***')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})])
@patch('requests.get', side_effect=[mock_response_dict(200)])
@patch('builtins.input', side_effect=['1', 'pallas', 'commonPass', '0', '0'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_password(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_print.assert_any_call('*** SIGN-IN ***')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('*** FLEA-MARKET ***')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input', side_effect=['1', 'pallas', 'antony98', '0', '0'])
@patch('builtins.print')
def test_app_item_list(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        main('__main__')
    mocked_print.assert_any_call('*** SIGN-IN ***')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('*** FLEA-MARKET ***')
    mocked_requests_get.assert_called_once_with(url='http://localhost:8000/api/v1/item/', headers={
        'Authorization': 'Token e2cd07584740609b17b0b0f2ce6787452aa801e0'})
    mocked_input.assert_called()


@patch('requests.delete', side_effect=[mock_response_dict(200)])
@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})
                                     ])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 6,
                                                             'name': 'davide',
                                                             'description': '.',
                                                             'condition': 0,
                                                             'brand': 'nike',
                                                             'price': 200,
                                                             'category': 'ciccio'}])])
@patch('builtins.input',
       side_effect=['1', 'udonto', 'fazio9898',  '2', '1'])
@patch('builtins.print')
def test_app_remove_item(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post, mocked_requests_delete):
    with patch('builtins.open', mock_open()) as mocked_open:
        main('__main__')
    assert list(filter(lambda x: 'Item removed!' in str(x), mocked_print.mock_calls))
    mocked_requests_delete.assert_called_with(url='http://localhost:8000/api/v1/item/edit/6', headers={
        'Authorization': 'Token e2cd07584740609b17b0b0f2ce6787452aa801e0'})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input', side_effect=['1', 'udonto', 'fazio9898', '2', '0'])
@patch('builtins.print')
def test_app_remove_item_operation_cancelled(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        main('__main__')
    assert list(filter(lambda x: 'Cancelled!' in str(x), mocked_print.mock_calls))

'''


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'ciao',
                                                              'description': 'Smartphone',
                                                              'condition': '0',
                                                              'brand': 'nike',
                                                              'price': '20',
                                                              'category': 'scarpe'})])
@patch('requests.get', side_effect=[mock_response(200, [])])
@patch('builtins.input',
       side_effect=['1', 'pallas', 'antony98', '1', 'ciao', 'Smartphone', '0', 'nike', '20', 'scarpe'])
@patch('builtins.print')
def test_app_add_item(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        main('__main__')
    assert list(filter(lambda x: 'Item added!' in str(x), mocked_print.mock_calls))
    assert list(filter(lambda x: '*** FLEA-MARKET ***' in str(x), mocked_print.mock_calls))

    #mocked_print.assert_any_call('*** FLEA-MARKET ***')

    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/item/add/', headers={
        'Authorization': 'Token e2cd07584740609b17b0b0f2ce6787452aa801e0'}, data={
        'name': 'ciao',
        'description': 'Smartphone',
        'condition': '0',
        'brand': 'nike',
        'price': '20',
        'category': 'scarpe'})





@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})])
@patch('requests.get', side_effect=[mock_response_dict(200)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '0', '0'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_username(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('*** SIGN IN ***')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_input.assert_called()
    mocked_print.assert_any_call('*** SHOPPING LIST ***')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef5f26'})])
@patch('requests.get', side_effect=[mock_response_dict(200)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'notSecurePassword', 'ciccioRiccio9!', '0', '0'])
@patch('builtins.print')
def test_app_sign_in_resists_wrong_password(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('*** SIGN IN ***')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('*** SHOPPING LIST ***')


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio19', 'ciccioRiccio9!'])
@patch('builtins.print')
def test_app_sign_in_nonexistent_user(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('This user does not exist!')


@patch('requests.post', side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['2', 'ciccioRiccio99', 'ciccio@esiste.it', 'ciccioRiccio9!'])
@patch('builtins.print')
def test_app_registration_existent_user(mocked_print, mocked_input, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_requests_post.assert_called()
    mocked_print.assert_any_call('This user already exists!')


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '0', '0'])
@patch('builtins.print')
def test_app_shopping_list(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()):
        App().run()
    mocked_print.assert_any_call('*** SIGN IN ***')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('*** SHOPPING LIST ***')
    mocked_requests_get.assert_called_once_with(url='http://localhost:8000/api/v1/shopping-list/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'})
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                         'name': 'Redmi Note 8',
                                                         'category': 'Smartphone',
                                                         'manufacturer': 'Xiaomi',
                                                         'price': 90000,
                                                         'description': '',
                                                         'quantity': 2},
                                                        {'id': 2,
                                                         'name': 'Macbook',
                                                         'category': 'Computer',
                                                         'manufacturer': 'Apple',
                                                         'price': 90000,
                                                         'description': '',
                                                         'quantity': 1}])])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '0', '0'])
@patch('builtins.print')
def test_app_shopping_list_load(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    main('__main__')
    mocked_print.assert_any_call('*** SIGN IN ***')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('*** SHOPPING LIST ***')
    mocked_requests_get.assert_called_once_with(url='http://localhost:8000/api/v1/shopping-list/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'})
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                         'name': 'Redmi M3',
                                                         'category': 'Tablet',
                                                         'manufacturer': 'Xiaomi',
                                                         'price': 54300,
                                                         'description': '',
                                                         'quantity': 2}])])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '0', '0'])
@patch('builtins.print')
def test_app_shopping_list_load_unknown_category(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    main('__main__')
    mocked_print.assert_any_call('*** SIGN IN ***')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('Continuing with an empty list of items...')
    mocked_print.assert_any_call('*** SHOPPING LIST ***')
    mocked_requests_get.assert_called_once_with(url='http://localhost:8000/api/v1/shopping-list/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'})
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(400)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '0', '0'])
@patch('builtins.print')
def test_app_shopping_fetch_server_error(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    main('__main__')
    mocked_print.assert_any_call('*** SIGN IN ***')
    mocked_print.assert_any_call('1:\tLogin')
    mocked_requests_post.assert_called()
    mocked_requests_get.assert_called()
    mocked_print.assert_any_call('Failed to connect to the server! Try later!')
    #sys.stdout.write(str(mocked_print.mock_calls))
    mocked_requests_get.assert_called_once_with(url='http://localhost:8000/api/v1/shopping-list/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'})
    mocked_input.assert_called()




@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Redmi Note 8',
                                                              'category': 'Smartphone',
                                                              'manufacturer': 'Xiaomi',
                                                              'price': 90000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200, [])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '1', 'Redmi Note 8', 'Xiaomi', '2', '900', '', '0', '0'])
@patch('builtins.print')
def test_app_add_smartphone(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Smartphone added!' in str(x), mocked_print.mock_calls))

    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Redmi Note 8',
        'category': 'Smartphone',
        'manufacturer': 'Xiaomi',
        'price': 90000,
        'description': '',
        'quantity': 2})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'P40 pro',
                                                              'category': 'Smartphone',
                                                              'manufacturer': 'Huawei',
                                                              'price': 90000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'P40',
                                                             'category': 'Smartphone',
                                                             'manufacturer': 'Huawei',
                                                             'price': 90000,
                                                             'description': '',
                                                             'quantity': 2}])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '1', 'P40 pro', 'Huawei', '2', '900', '', '1', 'P40 pro',
                    'Huawei', '2', '900', '', '0', '0'])
@patch('builtins.print')
def test_app_add_smartphone_with_duplicates(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Smartphone already present in the list!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'P40 pro',
        'category': 'Smartphone',
        'manufacturer': 'Huawei',
        'price': 90000,
        'description': '',
        'quantity': 2})

#sei super bellissimo
#
@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Mi 8 pro',
                                                              'category': 'Smartphone',
                                                              'manufacturer': 'Xiaomi',
                                                              'price': 90000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '1', '<script>', 'Mi 8 pro', 'Xiaomi', '2', '900', '', '0',
                    '0'])
@patch('builtins.print')
def test_app_add_smartphone_resists_wrong_name(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Smartphone added!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Mi 8 pro',
        'category': 'Smartphone',
        'manufacturer': 'Xiaomi',
        'price': 90000,
        'description': '',
        'quantity': 2})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Pocophone',
                                                              'category': 'Smartphone',
                                                              'manufacturer': 'Poco',
                                                              'price': 90000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '1', 'Pocophone', 'Poco', 'asd', '-1', '2', '900', '', '0',
                    '0'])
@patch('builtins.print')
def test_app_add_smartphone_resists_wrong_quantity(mocked_print, mocked_input, mocked_requests_get,
                                                   mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Smartphone added!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Pocophone',
        'category': 'Smartphone',
        'manufacturer': 'Poco',
        'price': 90000,
        'description': '',
        'quantity': 2})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Xperia z1',
                                                              'category': 'Smartphone',
                                                              'manufacturer': '',
                                                              'price': 90000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '1', 'Xperia z1', 'Sony', '2', 'asd', '-1', '900', '', '0',
                    '0'])
@patch('builtins.print')
def test_app_add_smartphone_resists_wrong_price(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Smartphone added!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Xperia z1',
        'category': 'Smartphone',
        'manufacturer': 'Sony',
        'price': 90000,
        'description': '',
        'quantity': 2})


@patch('requests.delete', side_effect=[mock_response_dict(200)])
@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})
                                     ])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Xperia z1',
                                                             'category': 'Smartphone',
                                                             'manufacturer': 'Sony',
                                                             'price': 90000,
                                                             'description': '',
                                                             'quantity': 2}])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!',  '3', '1', '0', '0'])
@patch('builtins.print')
def test_app_remove_item(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post, mocked_requests_delete):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Item removed!' in str(x), mocked_print.mock_calls))
    mocked_requests_delete.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/edit/1', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '3', '0', '0', '0'])
@patch('builtins.print')
def test_app_remove_item_operation_cancelled(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Operation cancelled!' in str(x), mocked_print.mock_calls))


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response_dict(200)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '4', '0', '0', '0'])
@patch('builtins.print')
def test_app_change_quantity_operation_cancelled(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Operation cancelled!' in str(x), mocked_print.mock_calls))


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Mi Air',
                                                              'category': 'Computer',
                                                              'manufacturer': 'Xiaomi',
                                                              'price': 40000,
                                                              'description': 'really excellent product',
                                                              'quantity': 1})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input', side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '2', 'Mi Air', 'Xiaomi', '1', '400',
                                      'really excellent product', '0', '0'])
@patch('builtins.print')
def test_app_add_computer(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Computer added!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Mi Air',
        'category': 'Computer',
        'manufacturer': 'Xiaomi',
        'price': 40000,
        'description': 'really excellent product',
        'quantity': 1})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Macbook',
                                                              'category': 'Computer',
                                                              'manufacturer': 'Apple',
                                                              'price': 100000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Macbook',
                                                             'category': 'Computer',
                                                             'manufacturer': 'Apple',
                                                             'price': 100000,
                                                             'description': '',
                                                             'quantity': 2}])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!','2', 'Macbook',
                    'Apple', '2', '1000', '', '0', '0'])
@patch('builtins.print')
def test_app_add_computer_with_duplicates(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Computer already present in the list!' in str(x), mocked_print.mock_calls))



@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Magicbook',
                                                              'category': 'Computer',
                                                              'manufacturer': 'Huawei',
                                                              'price': 65030,
                                                              'description': '',
                                                              'quantity': 5})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '2', '<script>', 'Magicbook', 'Huawei', '5', '650.30', '',
                    '0', '0'])
@patch('builtins.print')
def test_app_add_computer_resists_wrong_name(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Computer added!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Magicbook',
        'category': 'Computer',
        'manufacturer': 'Huawei',
        'price': 65030,
        'description': '',
        'quantity': 5})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Msv330',
                                                              'category': 'Computer',
                                                              'manufacturer': 'Msi',
                                                              'price': 90000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '2', 'Msv330', 'Msi', 'asd', '-1', '2', '900', '', '0',
                    '0'])
@patch('builtins.print')
def test_app_add_computer_resists_wrong_quantity(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Computer added!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Msv330',
        'category': 'Computer',
        'manufacturer': 'Msi',
        'price': 90000,
        'description': '',
        'quantity': 2})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'}),
                                     mock_response_dict(200, {'id': 1,
                                                              'name': 'Sxs500v',
                                                              'category': 'Computer',
                                                              'manufacturer': 'Asus',
                                                              'price': 90000,
                                                              'description': '',
                                                              'quantity': 2})])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '2', 'Sxs500v', 'Asus', '2', 'asd', '-1', '900', '', '0',
                    '0'])
@patch('builtins.print')
def test_app_add_computer_resists_wrong_price(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'Computer added!' in str(x), mocked_print.mock_calls))
    mocked_requests_post.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/add/', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={
        'name': 'Sxs500v',
        'category': 'Computer',
        'manufacturer': 'Asus',
        'price': 90000,
        'description': '',
        'quantity': 2})


@patch('requests.delete', side_effect=[mock_response_dict(200)])
@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Xperia z1',
                                                             'category': 'Smartphone',
                                                             'manufacturer': 'Sony',
                                                             'price': 90000,
                                                             'description': '',
                                                             'quantity': 2}])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '3', '4', '1',
                    '0', '0'])
@patch('builtins.print')
def test_app_remove_item_resists_wrong_index(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post,
                                             mocked_requests_delete):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()
    assert list(filter(lambda x: 'Item removed!' in str(x), mocked_print.mock_calls))
    mocked_requests_delete.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/edit/1', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'})


@patch('requests.patch', side_effect=[mock_response_dict(200)])
@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Pixel',
                                                             'category': 'Smartphone',
                                                             'manufacturer': 'Google',
                                                             'price': 97320,
                                                             'description': '',
                                                             'quantity': 1}])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '4', '1', '5',
                    '0', '0'])
@patch('builtins.print')
def test_app_change_quantity(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post,
                             mocked_requests_patch):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()
    assert list(filter(lambda x: 'Quantity changed!' in str(x), mocked_print.mock_calls))
    mocked_requests_patch.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/edit/1', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={'quantity': 5})


@patch('requests.patch', side_effect=[mock_response_dict(200)])
@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Pixel',
                                                             'category': 'Smartphone',
                                                             'manufacturer': 'Google',
                                                             'price': 97320,
                                                             'description': '',
                                                             'quantity': 1}])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!',  '4', '-1', '1',
                    '5', '0', '0'])
@patch('builtins.print')
def test_app_change_quantity_resists_wrong_index(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post,
                                                 mocked_requests_patch):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()
    assert list(filter(lambda x: 'Quantity changed!' in str(x), mocked_print.mock_calls))
    mocked_requests_patch.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/edit/1', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={'quantity': 5})


@patch('requests.patch', side_effect=[mock_response_dict(200)])
@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Pixel',
                                                             'category': 'Smartphone',
                                                             'manufacturer': 'Google',
                                                             'price': 97320,
                                                             'description': '',
                                                             'quantity': 1}])])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!','4', '1', '-1',
                    '5', '0', '0'])
@patch('builtins.print')
def test_app_change_quantity_resists_wrong_new_quantity(mocked_print, mocked_input, mocked_requests_get,
                                                        mocked_requests_post, mocked_requests_patch):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()
    assert list(filter(lambda x: 'Quantity changed!' in str(x), mocked_print.mock_calls))
    mocked_requests_patch.assert_called_with(url='http://localhost:8000/api/v1/shopping-list/edit/1', headers={
        'Authorization': 'Token 3be7163c1baea2a220777a82ec7e59a4ef545f26'}, data={'quantity': 5})


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Mi Air',
                                                             'category': 'Computer',
                                                             'manufacturer': 'Xiaomi',
                                                             'price': 40000,
                                                             'description': '',
                                                             'quantity': 1},
                                                            {'id': 2,
                                                             'name': 'Mac',
                                                             'category': 'Computer',
                                                             'manufacturer': 'Apple',
                                                             'price': 1,
                                                             'description': '',
                                                             'quantity': 1}])
                                    ])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '6', '0', '0'])
@patch('builtins.print')
def test_app_sort_by_price(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()
    assert list(filter(lambda x: '1   Computer                       Mac' in str(x), mocked_print.mock_calls))


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '3be7163c1baea2a220777a82ec7e59a4ef545f26'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                             'name': 'Mi Air',
                                                             'category': 'Computer',
                                                             'manufacturer': 'Xiaomi',
                                                             'price': 40000,
                                                             'description': '',
                                                             'quantity': 1},
                                                             {'id': 2,
                                                             'name': 'Mac',
                                                             'category': 'Computer',
                                                             'manufacturer': 'Apple',
                                                             'price': 1,
                                                             'description': 'really excellent product',
                                                             'quantity': 1}])
                                    ])
@patch('builtins.input',
       side_effect=['1', 'ciccioRiccio99', 'ciccioRiccio9!', '5', '0', '0'])
@patch('builtins.print')
def test_app_sort_by_manufacturer(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()

    mocked_input.assert_called()
    mocked_print.assert_called()
    assert list(filter(lambda x: '1   Computer                       Mac' in str(x), mocked_print.mock_calls))
'''
