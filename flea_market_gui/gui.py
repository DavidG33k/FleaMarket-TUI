from typing import Callable, Any

import PySimpleGUI as sg
import requests
from valid8 import ValidationError

from flea_market_tui.domain import Username, Password

sg.theme('DarkPurple1')
api_address = 'http://localhost:8000/api/v1/'

def progress_bar():
    layout = [[sg.Text('Creating your account...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()

def first_menu():
    layout = [[sg.Button('Login', size=30)],
              [sg.Button('Registration', size=30)],
              [sg.Button('Exit', size=30)]]

    window = sg.Window("FleaMarket", layout)

    while True:
        event,values = window.read()

        if event == 'Login':
            window.close()
            login()
            break
        if event == 'Registration':
            window.close()
            create_account()
            break
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

    window.close()

def create_account():
    global username, password

    layout = [[sg.Text("Sign Up", size =(15, 1), font=40, justification='c')],
             [sg.Text("Username", size =(13, 1), font=14), sg.InputText(key='-username-', font=14)],
             [sg.Text("E-mail", size=(13, 1), font=14), sg.InputText(key='-email-', font=14)],
             [sg.Text("Password", size =(13, 1), font=14), sg.InputText(key='-password-', font=14, password_char='*')],
             [sg.Button("Submit"), sg.Button("Cancel")]]

    window = sg.Window("Sign Up", layout)

    while True:
        event,values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Submit":
                password = values['-password-']
                username = values['-username-']
                if values['-email-'] != values['-remail-']:
                    sg.popup_error("Error", font=16)
                    continue
                elif values['-email-'] == values['-remail-']:
                    progress_bar()
                    break
    window.close()

def login():
    global username,password

    layout = [[sg.Text("Log In", size =(15, 1), font=40, justification='r')],
            [sg.Text("Username")],
            [sg.InputText(key='-username-')],
            [sg.Text(key='-err1-')],
            [sg.Text("Password")],
            [sg.InputText(key='-password-', password_char='*')],
            [sg.Text(key='-err2-')],
            [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window("Log In", layout)

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            first_menu()
            break
        else:
            if event == "Ok":
                username = __build_input(values['-username-'], Username)
                password = __build_input(values['-password-'], Password)

                res = requests.post(url=f'{api_address}auth/login/', data={'username': username, 'password': password})

                if res.status_code != 200:
                    sg.Popup('User does not exist :( Please retry!')
                    window.close()
                    login()
                #self.__key = res.json()['key']
                return True

    window.close()


def __build_input(input_string, builder: Callable) -> Any:  # Implemented to erase exceptions in real time.
    try:
        res = builder(input_string.strip())
        return res
    except (TypeError, ValueError, ValidationError) as e:
        sg.Popup(e)


#  _____________MAIN_____________
def main(name: str):
    if name == '__main__':
        first_menu()


main(__name__)