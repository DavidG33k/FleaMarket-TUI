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


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'e2cd07584740609b17b0b0f2ce6787452aa801e0'})])
@patch('requests.get', side_effect=[mock_response(200, [{'id': 1,
                                                         'name': 'weqweq',
                                                         'description': 'bello',
                                                         'condition': 2,
                                                         "brand": "aaaa",
                                                         'price': 90000,
                                                         'category': 'sfrrewes'},
                                                        {'id': 2,
                                                         'name': 'wsssseqweq',
                                                         'description': 'bssssello',
                                                         'condition': 1,
                                                         "brand": "aaadddda",
                                                         'price': 900,
                                                         'category': 'scdefrrewes'}])])
@patch('builtins.input', side_effect=['1', 'udonto', 'fazio9898', '0', '0'])
@patch('builtins.print')
def test_load_fleamarket_app(mocked_print, mocked_input, mocked_requests_get, mocked_requests_post):
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
                                                             'category': 'ciccio',
                                                             }])])
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

