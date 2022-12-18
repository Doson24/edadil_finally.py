import datetime

a = ['89,99 ₽\n130,40 ₽']
a = a[0].split('\n')
date = datetime.date.today()

with open("Список_покупок.txt", "r", encoding="utf-8") as list_open:
    request_list = list_open.read().split(',')



print(request_list[0])