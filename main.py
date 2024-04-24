from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem


class MDNavigationRail(MDNavigationRail): #не меняет тему, при нажатии на кнопку появляется ошибка
    def open_drop_item_menu(self, item): #открывает меню
            menu_items = [
                {
                    "text": "Сменить тему",
                    "on_release": lambda x= 1 : DemoApp.change_theme(item)
                }
            ]
            self.drop_item_menu = MDDropdownMenu(
                caller=item, items=menu_items, position="center"
            )
            self.drop_item_menu.open()
        #если хочешь обратиться к функции на данном экране, то нужно написать root.(назвние ф-ции)(self)
        #некоторые ф-ции можно вызвать ток в MDApp, например change_theme

class Screens(ScreenManager):
    pass


class MenuScreen(Screen):
    pass


class CommonNavigationRailItem(MDNavigationRailItem):
    text = StringProperty()
    icon = StringProperty()


class ProfileScreen(Screen):
    pass


sm = ScreenManager(transition=NoTransition()) 
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(MenuScreen(name='menu_screen'))




class DemoApp(MDApp):
    def change_theme(self): #меняет тему
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.primary_palette = "Rosybrown"
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Orange"
    
    

    def build(self):
        return Builder.load_file('layouts.kv')


DemoApp().run()
