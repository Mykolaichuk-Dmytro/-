greeting = "Hello world"
first_name = "Дмитро"
last_name = "Миколайчук"
age = 16

if type(first_name) == type(last_name):
    print("Ім'я та прізвище мають однаковий тип даних:", type(first_name))

name_list = [f"{first_name} {last_name}"]

if isinstance(age, int):
    print("Тип даних віку:", type(age))

print("Список ім'я і прізвище:", name_list)
