from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import*
import os
import sqlite3
import datetime as dt

Builder.load_file('manager.kv')
login = "admin"
# основной экран
class MainMenu(Screen):

    box = ObjectProperty()

    def create_Bd(): # создаём БД 
        global database
        global cursor
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, 'Logins.db')
        database = sqlite3.connect(file_path) 
        cursor = database.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
            login Text,
            name TEXT,
            main TEXT,
            priority INTEGER,
            data INTEGER
        )""")
        database.commit()

    def Add_button(self): # добавление новых кнопок ( тут не используем ее)
        self.but_open2 = Button (text = 'Ещё', font_size = 20) 
        self.but_open2.on_release = self.Add_button
        self.box.add_widget(self.but_open2)

    def show_tasks(self): # Показывает все таски
        print("Tasks:")
        for task in cursor.execute(""" SELECT * FROM tasks"""):
            print(task[:-1], New_task.get_data(task[-1]))


class New_task(Screen):

    name_t = ObjectProperty()
    main_t = ObjectProperty()
    priority_t = ObjectProperty()
    data_t = ObjectProperty()

    def make(self): # Проверяем данные и записываем в БД
        print(self.name_t.text, self.main_t.text, self.priority_t.text, self.data_t.text)
        if not self.priority_t.text.isdigit():
            print("Приоритет должен быть числом")
        # ещё нужна проверка на корректную дату
        else:
            day, month, year = self.data_t.text.split('.')
            data = self.timestamp(int(day), int(month), int(year))
            cursor.execute(f"INSERT INTO tasks VALUES (?, ?, ?, ?, ?)", (login, self.name_t.text, 
            self.main_t.text, self.priority_t.text, data))
            database.commit()
            self.manager.current = 'MainMenu'

    def timestamp(self, d, m, y): # из даты в число
        return dt.datetime.timestamp(dt.datetime(y, m, d))

    def get_data(tmstmp): # из числа в дату
        return dt.datetime.fromtimestamp(tmstmp).date()


class managerApp(App):
    def build(self):

        MainMenu.create_Bd()

        ScrManager = ScreenManager(transition = SlideTransition()) # Изменение переходов
        screens = [
            MainMenu(name = "MainMenu"),
            New_task(name = "new_task"),
        ]
        for i in screens:
            ScrManager.add_widget(i)
        return ScrManager
        

if __name__ == "__main__":
    managerApp().run()
