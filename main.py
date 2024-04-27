from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

auth = "N2E3OWRiZDQtM2NlZi00OTQ2LTg2NmMtMjc3MzIwMDRjZDZjOjVmMzA5N2ZiLTAzNWUtNGJiYS05MjNmLWNjNGQzZWIxNWEwZA=="

giga = GigaChat(credentials=auth,
                model='GigaChat:latest',
                verify_ssl_certs=False
                )

# создадим список, где будем хранить сообщения
# системное сообщение идет первым в списке (если, конечно, оно есть)

msgs = [
    SystemMessage(content='')
]

while True:
  user_input = input("Пользователь: ")
  if user_input == 'СТОП':
    break
  msgs.append(HumanMessage(content=user_input))
  answer = giga(msgs)
  msgs.append(answer)
  print('GigaChat:', answer.content)
