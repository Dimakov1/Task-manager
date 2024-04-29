from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
import sqlite3
from kivy.properties import ObjectProperty
import os



class RailScreen(Screen):  
    def open_drop_item_menu(self, item):  # открывает меню
        menu_items = [
            {
                "text": "Сменить тему",
                "on_release": lambda x=1: DemoApp.change_theme(item)
            }
        ]
        self.drop_item_menu = MDDropdownMenu(
            caller=item, items=menu_items, position="center"
        )
        self.drop_item_menu.open()
    # если хочешь обратиться к функции на данном экране, то нужно написать root.(назвние ф-ции)(self)
    # некоторые ф-ции можно вызвать ток в MDApp, например change_theme


class Screens(ScreenManager):
    pass

class Login(Screen): #включить функции по регистрации (бэк)

    def create_Bd(): # создаём БД 
        global database
        global cursor
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, 'Logins.db')
        database = sqlite3.connect(file_path) 
        cursor = database.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            login TEXT,
            password TEXT
        )""")
        database.commit()
    
    input_login = ObjectProperty() # TextInput для логина
    input_password = ObjectProperty() # TextInput для пароля

    def login_user(self): # Проверка данных и вход
        if cursor.execute(f"SELECT login FROM users WHERE login = '{self.input_login.text}'").fetchone() is None:
            print("Такого пользователя не существует") 
        elif cursor.execute(f"SELECT login, password FROM users WHERE login = '{self.input_login.text}'").fetchone()[1] != self.input_password.text:
            print("Неверный пароль")
        else:
            print("вход осуществлен")
            self.manager.current = 'rail_screen'


# Экран регистрации
class Register(Screen):
    
    login_t = ObjectProperty() # TextInput для логина
    password_t = ObjectProperty() # TextInput для пароля
    password_t2 = ObjectProperty() # TextInput для второго пароля

    def register(self): # проверка данных и запись в БД
        print(self.login_t.text, self.password_t.text, self.password_t2.text)
        if len(self.login_t.text) <= 4:
            print("Логин должен содержать более 4 символов")
        elif len(self.password_t.text) <= 4:
            print("Пароль должен содержать более 4 символов")
        elif self.password_t.text != self.password_t2.text:
            print("Пароли не совпадают")
        elif cursor.execute(f"SELECT login FROM users WHERE login = '{self.login_t.text}'").fetchone() is not None:
            print("Такой пользователь уже существует")
        else:
            cursor.execute(f"INSERT INTO users VALUES (?, ?)", (self.login_t.text, self.password_t.text))
            database.commit()
            print("всё гуд")
            # TextInput'ы очищаем и переходим на экран логина
            self.login_t.text, self.password_t.text, self.password_t2.text = '', '', ''
            self.manager.current = 'login'


class MenuScreen(Screen):
    pass

class FieldText(MDTextField):
    icon = StringProperty()
    hint_text = StringProperty()

class CommonNavigationRailItem(MDNavigationRailItem):
    text = StringProperty()
    icon = StringProperty()


class ProfileScreen(Screen):
    pass




class DemoApp(MDApp):
    def change_theme(self):  # меняет тему
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.primary_palette = "Rosybrown"
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Orange"

    def build(self):
        Login.create_Bd()
        return Builder.load_file('new_screen.kv')


DemoApp().run()
