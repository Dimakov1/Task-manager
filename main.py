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
from kivy.properties import BooleanProperty
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivymd.uix.list import MDListItemTrailingIcon
import os
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.pickers import MDDockedDatePicker
import datetime
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
import pyperclip

from kivymd.uix.widget import MDWidget
from database import Database

db = Database()

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)

Window.size = (800, 670)


class TaskScreen(Screen):  # Создаем класс TaskScreen, наследующийся от Screen

    def build(self):
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("add_task.kv")

    def close_window(self):
        self.manager.current = 'tasks'


class AddTask(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_dialog_open = False

    def add_task(self):
        self.date_dialog_open = True
        if self.ids.date_picker.text != "":
            task_dl = self.ids.date_picker.text
        else:
            task_dl = "no deadline"

        task_id = db.create_task(user_id, self.new_task_name.text, self.new_task_description.text, task_dl)

        task_screen = self.manager.get_screen('tasks')
        task_screen.ids.tasks.add_widget(ExpansionPanelItem(
            header_text=f"{self.new_task_name.text}",
            description=f"{self.new_task_description.text}",
            support_text=f"{task_dl}",
            task_id=str(task_id[0])
        ))

        self.new_task_name.text = ''
        self.new_task_description.text = ''
        self.ids.date_picker.focus = True
        self.ids.date_picker.focus = False
        self.ids.date_picker.text = ''
        self.date_dialog_open = False
        self.end = 0
        Login.count_add(self)

    def add_to_favorite_task(task_id):
        db.mark_task_as_important(user_id, task_id)

    def delete_from_favorite_task(task_id):
        db.mark_task_as_unimportant(user_id, task_id)

    def add_to_completed_task(task_id):
        db.mark_task_as_complete(user_id, task_id)

    def delete_from_completed_task(task_id):
        db.mark_task_as_incomplete(user_id, task_id)

    def show_date_picker(self):
        self.end = 0
        if self.date_dialog_open or self.end:
            return
        self.date_dialog_open = True

        date_dialog = MDDockedDatePicker(min_date=datetime.date.today(), max_date=datetime.date(
            datetime.date.today().year + 10,
            datetime.date.today().month,
            datetime.date.today().day,
        ))
        date_dialog.pos = [
            self.ids.date_picker.center_x - date_dialog.width / 2,
            self.ids.date_picker.y - date_dialog.height / 2,
        ]
        date_dialog.bind(on_ok=self.on_ok, on_cancel=self.on_cancel, on_dismiss=self.on_dismiss)
        date_dialog.open()

    def on_ok(self, instance):
        self.ids.date_picker.text = str(instance.get_date()[0])
        global task_dl
        task_dl = self.ids.date_picker.text

        instance.dismiss()

    def on_cancel(self, instance):
        self.date_dialog_open = False
        self.ids.date_picker.focus = False
        instance.dismiss()

    def on_dismiss(self, instance):
        self.ids.date_picker.focus = False
        self.date_dialog_open = False


class FavoriteTasks(Screen):
    def show(self):
        user_tasks = db.get_favorite_tasks(user_id)
        self.manager.get_screen('favorite_tasks').ids.ftasks.clear_widgets()
        for i in user_tasks:
            self.manager.get_screen('favorite_tasks').ids.ftasks.add_widget(ExpansionPanelItem(
                header_text=f"{i[1]}",
                description=f"{i[2]}",
                support_text=f"{i[3]}",
                task_id=f"{i[0]}",
                is_favorite=bool(i[4]),
                is_completed=bool(i[5])

            ))
            print(f"Added favorite task: {str(i)}")

    def delete_from_favorite(self):
        pass


class CompletedTasks(Screen):
    def show(self):
        user_tasks = db.get_completed_tasks(user_id)
        self.manager.get_screen('completed_tasks').ids.ctasks.clear_widgets()
        for i in user_tasks:
            self.manager.get_screen('completed_tasks').ids.ctasks.add_widget(ExpansionPanelItem(
                header_text=f"{i[1]}",
                description=f"{i[2]}",
                support_text=f"{i[3]}",
                task_id=f"{i[0]}",
                is_favorite=bool(i[4]),
                is_completed=bool(i[4])
            ))
            print(f"Added completed task: {str(i)}")

    def delete_from_completed(self):
        pass

class MenuScreen(Screen):

    def delete(self):
        pass


class RailScreen(Screen):
    text = StringProperty()
    old_instance_active = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.item_1.bind(on_touch_down=self.on_nav_item_touch)
        self.ids.item_2.bind(on_touch_down=self.on_nav_item_touch)
        self.ids.item_3.bind(on_touch_down=self.on_nav_item_touch)
        self.ids.item_4.bind(on_touch_down=self.on_nav_item_touch)
        self.ids.item_5.bind(on_touch_down=self.on_nav_item_touch)


    def change_screen(self, screen_name):
        self.ids.right_screen_manager.current = screen_name

    def on_nav_item_touch(self, instance, touch):
        if (instance.collide_point(*touch.pos)):
            instance.on_touch_down(touch)
            current_screen = self.ids.right_screen_manager.current
            instance.active = True
            instance.active = False
            if instance.text == 'favorite_tasks' and current_screen != instance.text:
                self.show_favorite_tasks()
                self.change_screen(instance.text)


            elif instance.text == 'completed_tasks' and current_screen != instance.text:
                self.show_completed_tasks()
                self.change_screen(instance.text)

            elif instance.text == 'gpt_screen' and current_screen != instance.text:
                self.change_screen(instance.text)

            elif instance.text == 'tasks' and current_screen != instance.text:
                self.show()
                self.change_screen(instance.text)

            elif instance.text == 'profile_screen' and current_screen != instance.text:
                self.change_screen(instance.text)


            return True
        return False



    def open_drop_item_menu(self, item):
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


    def show(self):  # тут закидываем таски на экран TaskScreen
        task_screen = self.manager.get_screen('rail_screen').ids.right_screen_manager
        task_screen = task_screen.get_screen('tasks')
        task_screen.ids.tasks.clear_widgets()
        user_tasks = db.get_tasks(user_id)
        for i in user_tasks[0]:
            task_screen.ids.tasks.add_widget(ExpansionPanelItem(
                header_text=f"{i[1]}",
                description=f"{i[2]}",
                support_text=f"{i[3]}",
                task_id=f"{i[0]}",
                is_favorite=bool(i[4]),
                is_completed=bool(i[5])
            ))
            print(i)


    def show_completed_tasks(self):
        completed_tasks_screen = self.manager.get_screen('rail_screen').ids.right_screen_manager
        user_tasks = db.get_completed_tasks(user_id)
        completed_tasks_screen.get_screen('completed_tasks').ids.ctasks.clear_widgets()
        for i in user_tasks:
            completed_tasks_screen.get_screen('completed_tasks').ids.ctasks.add_widget(ExpansionPanelItem(
                header_text=f"{i[1]}",
                description=f"{i[2]}",
                support_text=f"{i[3]}",
                task_id=f"{i[0]}",
                is_favorite=bool(i[4]),
                is_completed=bool(i[5])
            ))
          
    def show_favorite_tasks(self):
        favorite_tasks_screen = self.manager.get_screen('rail_screen').ids.right_screen_manager
        user_tasks = db.get_favorite_tasks(user_id)
        favorite_tasks_screen.get_screen('favorite_tasks').ids.ftasks.clear_widgets()
        for i in user_tasks:
            favorite_tasks_screen.get_screen('favorite_tasks').ids.ftasks.add_widget(ExpansionPanelItem(
                header_text=f"{i[1]}",
                description=f"{i[2]}",
                support_text=f"{i[3]}",
                task_id=f"{i[0]}",
                is_favorite=bool(i[4]),
                is_completed=bool(i[5])
            ))

    def show_all_tasks(self):  # тут закидываем таски на экран TaskScreen
        task_screen = self.manager.get_screen('rail_screen').ids.right_screen_manager
        user_tasks = db.get_tasks(user_id)
        task_screen.get_screen('tasks').ids.tasks.clear_widgets()
        for i in user_tasks[0]:
            task_screen.get_screen('tasks').ids.tasks.add_widget(ExpansionPanelItem(
                header_text=f"{i[1]}",
                description=f"{i[2]}",
                support_text=f"{i[3]}",
                task_id=f"{i[0]}",
                is_favorite=bool(i[4]),
                is_completed=bool(i[5])
            ))
            print(i)


class CompletedTasks(Screen):
    pass

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
            password TEXT,
            user_id INTEGER,
            add_c INTEGER DEFAULT 0,
            delete_c INTEGER DEFAULT 0
        )""")
        database.commit()

    input_login = ObjectProperty()  # TextInput для логина
    input_password = ObjectProperty()  # TextInput для пароля

    def login_user(self):  # Проверка данных и вход
        if cursor.execute(f"SELECT login FROM users WHERE login = '{self.input_login.text}'").fetchone() is None:
            MDSnackbar(
                MDSnackbarText(
                    text="Такого пользователя не существует",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
        elif cursor.execute(f"SELECT login, password FROM users WHERE login = '{self.input_login.text}'").fetchone()[
            1] != self.input_password.text:
            MDSnackbar(
                MDSnackbarText(
                    text="Неверный пароль",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
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
            global user_id
            user_id = int(
                cursor.execute(f"SELECT user_id FROM users WHERE login = '{self.input_login.text}'").fetchone()[0])
            self.manager.current = 'rail_screen'
            RailScreen.show


    def count_add(self):
        print(cursor.execute(f"SELECT add_c FROM users").fetchone())
        cursor.execute("UPDATE users SET add_c = add_c + 1 WHERE user_id = ?", (user_id,))
        database.commit()

    def count_delete(self):
        cursor.execute("UPDATE users SET delete_c = delete_c + 1 WHERE user_id = ?", (user_id,))
        database.commit()
    
    def show_login(self):
        return cursor.execute(f"SELECT login FROM users WHERE user_id = user_id").fetchone()[0]
    
    def show_del(self):
        return cursor.execute(f"SELECT delete_c FROM users").fetchone()[0]
    
    def show_ad(self):
        return cursor.execute(f"SELECT add_c FROM users").fetchone()[0]



# Экран регистрации
class Register(Screen):
    login_t = ObjectProperty()  # TextInput для логина
    password_t = ObjectProperty()  # TextInput для пароля
    password_t2 = ObjectProperty()  # TextInput для второго пароля

    def register(self):  # проверка данных и запись в БД
        print(self.login_t.text, self.password_t.text, self.password_t2.text)
        if len(self.login_t.text) <= 4:
            MDSnackbar(
                MDSnackbarText(
                    text="Логин должен содержать более 4 символов",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
        elif len(self.password_t.text) <= 4:
            MDSnackbar(
                MDSnackbarText(
                    text="Пароль должен содержать более 4 символов",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
        elif self.password_t.text != self.password_t2.text:
            MDSnackbar(
                MDSnackbarText(
                    text="Пароли не совпадают",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
        elif cursor.execute(f"SELECT login FROM users WHERE login = '{self.login_t.text}'").fetchone() is not None:
            MDSnackbar(
                MDSnackbarText(
                    text="Такой пользователь уже существует",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
        else:
            global user_id
            if cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
                id = 0
            else:
                id = int(cursor.execute("SELECT MAX(user_id) FROM users").fetchone()[0])
            user_id = id + 1
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (self.login_t.text, self.password_t.text, user_id, 0, 0))
            database.commit()
            MDSnackbar(
                MDSnackbarText(
                    text="Вы успешно зарегистрировались",
                    theme_text_color="Custom",
                    text_color='white',
                ),
                background_color='#0e134f',
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
                radius=[(20)] * 4
            ).open()
            # TextInput'ы очищаем и переходим на экран логина
            self.login_t.text, self.password_t.text, self.password_t2.text = '', '', ''
            self.manager.current = 'login'


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    pass


class FieldText(MDTextField):
    text_color = ObjectProperty()
    icon = StringProperty()
    hinter = StringProperty()
    more_icon = StringProperty()
    color_up = ObjectProperty()
    value = ''
    dater = ObjectProperty()

    def check_text(self, bg_color, dater=0):
        if self.value == '':
            self.value = self.hinter
        if self.hint_txt.text:
            self.hinter = ""
            self.color_up = bg_color
            self.hint_txt.focus = False
            self.hint_txt.focus = True
        else:
            if dater:
                self.color_up = self.text_color
                self.hinter = self.value
                self.hint_txt.focus = False
                return
            self.color_up = self.text_color
            self.hinter = self.value
            self.hint_txt.focus = False
            self.hint_txt.focus = True


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
            value = self.user_input.text  # введеный текст
            if value != '':
                self.ids.chat_list.add_widget(
                    Command(text=value, size_hint_x=.5, halign='center'))  # Command вопрос, Response = ответ от гпт
                self.msgs.append(HumanMessage(content=value))
                self.answer = self.giga(self.msgs)  # Ответ
                self.msgs.append(self.answer)
                self.ids.chat_list.add_widget(Response(text=self.answer.content, size_hint_x=.8, halign='left'))
                self.ids.chat_list.add_widget(MDWidget())
                self.ids.chat_list.add_widget(MDWidget())

                self.ids.chat_list.add_widget(
                    MDBoxLayout(MDIconButton(icon='pencil', on_press = self.add_from_gpt), MDIconButton(icon='content-duplicate', on_press = self.copy_gpt), spacing=10,
                                orientation='horizontal', pos_hint={'center_x': .535}))  # доделать функции
        finally:
            self.ids.user.focus = True
            self.user_input.text = ''

    
    def copy_gpt(self, instance):
        pyperclip.copy(self.answer.content)

    def add_from_gpt(self, instance):
        print("ggg")
        self.manager.current = 'add_task'
        self.manager.get_screen('add_task').ids.new_task_description.text = self.answer.content

class CommonNavigationRailItem(MDNavigationRailItem):
    text = StringProperty()
    icon = StringProperty()


class ProfileScreen(Screen):
    def unfocus1(self):
        self.username.focus = False

    def unfocus2(self):
        self.mail.focus = False
    
    def func_show_login(self):
        return Login.show_login(self)
    
    def show_add(self):
        return Login.show_ad(self)

    def show_delete(self):
        return Login.show_del(self)

class ExpansionPanelItem(MDExpansionPanel):
    header_text = StringProperty()
    support_text = StringProperty()
    description = StringProperty()
    task_id = StringProperty()
    dialog = None  # Poka zaebal
    is_favorite = BooleanProperty(False)
    is_completed  = BooleanProperty(False)


    def show_description(self):
        print(self.description)

        description_field = MDLabel(
            text=self.description,
        )
        self.desk = MDDialog(
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Описание задачи"), #Можно и добавить сюда название, как считаешь нужным
            MDDialogSupportingText(
                text=self.description # сюда добавить надо описание
            )
        )
        self.desk.open()

    def on_kv_post(self, base_widget):
        self.ids.heart_checkbox.state = 'down' if self.is_favorite else 'normal'
        self.ids.complete.state = 'down' if self.is_completed else 'normal'


    def favorite_task_active(self, checkbox, state):
        if state == 'down':
            AddTask.add_to_favorite_task(self.task_id)
        else:
            AddTask.delete_from_favorite_task(self.task_id)
        print(self.task_id)


    def completed_task_active(self, checkbox, state):
        if state == 'down':
            AddTask.add_to_completed_task(self.task_id)
        else:
            AddTask.delete_from_completed_task(self.task_id)
        print(self.task_id)
    def changer(self):
        if self.dialog == None:
            self.header_text_field = MDTextField(
                text=self.header_text
            )
        self.description_text_field = MDTextField(
            text=self.description,
            size=('20sp', '20sp')
        )
        self.support_text_field = MDTextField(
            text=self.support_text,
            # on_focus=AddTask.show_date_picker(self)
        )

        self.dialog = MDDialog(
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Изменение задачи"),
            MDDialogContentContainer(
                self.header_text_field,
                self.description_text_field,
                self.support_text_field,
                spacing="15dp", orientation="vertical",
            ), MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Отмена"),
                    style="text",
                    ripple_effect=False,
                    on_press=self.close_dialog
                ),
                MDWidget(),
                MDButton(
                    MDButtonText(text="Подтвердить изменения"),
                    ripple_effect=False,
                    style="text",
                    on_press=self.change_task
                )),
            auto_dismiss=False,
        )
        self.dialog.open()

    def change_task(self, instance):
        print(self.header_text_field.text, self.description_text_field.text, self.support_text_field.text)
        db.update_task_details(user_id, self.task_id, self.header_text_field.text, self.description_text_field.text, self.support_text_field.text)

        #Здесь надо подшаманить, чтобы обновлялся экран тасков

        self.close_dialog(self)

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

    def for_delete(self):
        if self.dialog == None:
            self.dialog = MDDialog(
                # -----------------------Headline text-------------------------
                MDDialogHeadlineText(
                    text="Вы точно уверены, что хотите удалить задачу?"),
                MDDialogSupportingText(
                    text='Отменить изменения будет нельзя'
                ),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="Отмена"),
                        style="text",
                        ripple_effect=False,
                        on_press=self.close_dialog
                    ),
                    MDWidget(theme_focus_color='Custom', ),
                    MDButton(
                        MDButtonText(text="Подтвердить"),
                        ripple_effect=False,
                        style="text",
                        on_press=self.delete_task
                        # допилить функция для удаления
                    ),
                    spacing="8dp",
                ), auto_dismiss=False
            )
            self.dialog.open()

    def close_dialog(self, instance):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def delete_task(self, instance):  # должна удалять таск из бд и из экрана
        db.delete_task(user_id, self.task_id)
        self.parent.remove_widget(self)
        self.close_dialog(self)
        Login.count_delete(self)


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
                   'add_task.kv', 'task_screen.kv', 'gpt.kv', 'favorite_tasks.kv', 'completed_tasks.kv']
        for screen in screens:
            Builder.load_file(f'kivy/{screen}')

        sm_one = ScreenManager(transition=NoTransition())
        sm_one.add_widget(Login(name="login"))
        sm_one.add_widget(Register(name="register"))
        sm_one.add_widget(RailScreen(name="rail_screen"))

        return sm_one


if __name__ == "__main__":
    DemoApp().run()