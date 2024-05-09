from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.textfield import MDTextField
import sqlite3
from kivy.core.window import Window
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.list import MDListItemTrailingIcon
import os
from kivymd.uix.button import MDIconButton, MDButton
from kivy.uix.modalview import ModalView
from kivymd.uix.label import MDLabel

Window.size = (800, 670)


class RailScreen(Screen):  # не меняет тему, при нажатии на кнопку появляется ошибка
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
    def togpt(self):
        gpt = ScreensSecond.get_screen('gpt_screen')
        ScreensSecond.choice(gpt)


class Screens(ScreenManager):
    pass

class ScreensSecond(ScreenManager):
    def choice(self, screen):
        self.manager.current = screen


class Login(Screen):  # включить функции по регистрации (бэк)

    def create_Bd():  # создаём БД
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

    input_login = ObjectProperty()  # TextInput для логина
    input_password = ObjectProperty()  # TextInput для пароля

    def login_user(self):  # Проверка данных и вход
        if cursor.execute(f"SELECT login FROM users WHERE login = '{self.input_login.text}'").fetchone() is None:
            print("Такого пользователя не существует")
        elif cursor.execute(f"SELECT login, password FROM users WHERE login = '{self.input_login.text}'").fetchone()[
            1] != self.input_password.text:
            print("Неверный пароль")
        else:
            MDSnackbar(
                MDSnackbarText(
                    text="Вход успешно выполнен",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
            self.manager.current = 'rail_screen'



# Экран регистрации
class Register(Screen):
    login_t = ObjectProperty()  # TextInput для логина
    password_t = ObjectProperty()  # TextInput для пароля
    password_t2 = ObjectProperty()  # TextInput для второго пароля

    def register(self):  # проверка данных и запись в БД
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


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    pass


class MenuScreen(Screen):
    def show(self): #тут закидываем таски на экран TaskScreen
        task_screen = self.manager.get_screen('tasks')
        for i in range(10):
            task_screen.ids.tasks_.add_widget(ExpansionPanelItem(

                header_text=f"Задача {i}",
                description=f"Описание задачи {i}"
            ))


class FieldText(MDTextField):
    text_color = ObjectProperty()
    icon = StringProperty()
    hint_text = StringProperty()
    more_icon = StringProperty()

class GPT(Screen):
    user_input = ObjectProperty()


class CommonNavigationRailItem(MDNavigationRailItem):
    text = StringProperty()
    icon = StringProperty()

class ProfileScreen(Screen):
    pass

class TaskScreen(Screen):
    pass



class ExpansionPanelItem(MDExpansionPanel):
    header_text = StringProperty()
    support_text = StringProperty()
    description = StringProperty()

    def tap_expansion_chevron(
            self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton
    ):
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not panel.is_open
            else [0, 0, 0, 0],
            d=0.2,
        ).start(panel)
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = ObjectProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = ObjectProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17
class DemoApp(MDApp):

    def build(self):
        Login.create_Bd()
        self.theme_cls.backgroundColor = '#0D1117'
        return Builder.load_file('new_screen.kv')

    def change_theme(self):  # ПОЧИНИТЬ
        pass



if __name__ == "__main__":
    DemoApp().run()
