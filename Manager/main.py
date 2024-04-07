from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class Task_add(Popup):

    text_input = ObjectProperty()

    def create_task(self):
        print(self.text_input.text)
        Container.all_task.append(self.text_input.text)
        print(Container.all_task)


class Container(GridLayout):

    label_text = ObjectProperty()
    all_task = []

    def change_text(self):
        self.label_text.text = self.text_input.text

    def new_task(self):
        task = Task_add()
        task.open()


class MyApp(App):
    def build(self):
        return Container()


if __name__ == "__main__":
    MyApp().run()
