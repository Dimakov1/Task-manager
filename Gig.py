from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import*

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Токен
auth = "N2E3OWRiZDQtM2NlZi00OTQ2LTg2NmMtMjc3MzIwMDRjZDZjOjVmMzA5N2ZiLTAzNWUtNGJiYS05MjNmLWNjNGQzZWIxNWEwZA=="

giga = GigaChat(credentials=auth,
                model='GigaChat:latest',
                verify_ssl_certs=False
                )

        
Builder.load_file('manager.kv')


# основной экран
class MainMenu(Screen):
    input_text = ObjectProperty()  # TextInput для TextInput
    label_text = ObjectProperty()  # TextInput для Label
    def Chat(self):
        # реализация GigaChat
        msgs = [SystemMessage(content='')]
        #user_input = input("Пользователь: ")
        user_input = self.input_text.text
        msgs.append(HumanMessage(content=user_input))
        answer = giga(msgs)
        msgs.append(answer)
        #print('GigaChat:', answer.content)
        self.label_text.text = answer.content
        self.input_text.text = ""



class managerApp(App):
    def build(self):
        return MainMenu()
        

if __name__ == "__main__":
    managerApp().run()
