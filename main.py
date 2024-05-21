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
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import NoTransition
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import time



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
    # некоторые ф-ции можно вызвать ток в MDApp, например change_them

    def on_nav_item_pressed(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if isinstance(instance, MDNavigationRailItem):
                screen_name = instance.screen
                self.manager_2.current = screen_name



class Screens(ScreenManager):
    pass


class ScreensSecond(ScreenManager):
    pass


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
    def show(self):  # тут закидываем таски на экран TaskScreen
        task_screen = self.manager.get_screen('tasks')
        for i in range(10):
            task_screen.ids.tasks_.add_widget(ExpansionPanelItem(

                header_text=f"Задача {i}",
                description=f"Описание задачи {i}"
            ))


class FieldText(MDTextField):
    text_color = ObjectProperty()
    icon = StringProperty()
    hinter = StringProperty()
    more_icon = StringProperty()
    color_up = ObjectProperty()
    value = ''

    def check_text(self):
        if self.value == '':
            self.value = self.hinter
        if self.hint_txt.text:
            self.hinter = ""
            self.color_up = '#0D1117'
            self.hint_txt.focus = False
            self.hint_txt.focus = True
        else:
            self.color_up = 'white'
            self.hinter = self.value
            self.hint_txt.focus = False
            self.hint_txt.focus = True


class AddTask(Screen):
    pass  # ПОДКЛЮЧИТЬ БАЗУ ДАННЫХ ДЛЯ СОЗДАНИЯ НОВЫХ ТАСКОВ


class GPT(Screen):
    user_input = ObjectProperty()
    dialog = []
    # Токен
    auth = "N2E3OWRiZDQtM2NlZi00OTQ2LTg2NmMtMjc3MzIwMDRjZDZjOjVmMzA5N2ZiLTAzNWUtNGJiYS05MjNmLWNjNGQzZWIxNWEwZA=="
    giga = GigaChat(credentials=auth,
                model='GigaChat:latest',
                verify_ssl_certs=False
                )
    msgs = [SystemMessage(content='')]
    
    def send(self):  # димас тебе доделать, еще нужно постоянную фокусировску сделатб
        try:
            value = self.user_input.text # введеный текст
            if value != '':
                self.ids.chat_list.add_widget(
                    Command(text=value, size_hint_x=.2, halign='center'))  # Command вопрос, Response = ответ от гпт
                self.msgs.append(HumanMessage(content=value))
                answer = self.giga(self.msgs) # Ответ
                self.msgs.append(answer)
                self.ids.chat_list.add_widget(Response(text=answer.content, size_hint_x=.8, halign='center'))
        finally:
            self.ids.user.focus = True
            self.user_input.text = ''



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
        screens = ['classes.kv', 'login.kv', 'rail_screen.kv', 'register.kv', 'menu_screen.kv', 'profile.kv',
                   'add_task.kv', 'task_screen.kv', 'gpt.kv']
        for screen in screens:
            Builder.load_file(f'kivy/{screen}')
        sm_one = ScreenManager(transition=NoTransition())
        sm_one.add_widget(Login(name="login"))
        sm_one.add_widget(AddTask(name="add_task"))
        sm_one.add_widget(Register(name="register"))
        sm_one.add_widget(RailScreen(name="rail_screen"))
        return sm_one



    def change_theme(self):  # ПОЧИНИТЬ
        pass


if __name__ == "__main__":
    DemoApp().run()