import telebot


TOKEN = "7478569385:AAG7HoVnipiOSE23z_c0jRapkcDXwVQj8TM"
bot = telebot.TeleBot(TOKEN)

assortment = {
    '1': ("Кепка Basic", 200),
    '2': ("Кепка Premium", 300),
    '3': ("Кепка Спортивна", 400)
}

colors = {
    '1': "Чорний",
    '2': "Синій",
    '3': "Червоний",
    '4': "Білий"
}

prints = {
    '1': ("Без принта", 0),
    '2': ("Логотип", 50),
    '3': ("Індивідуальний дизайн", 100)
}

sizes = ['S', 'M', 'L', 'XL']

user_states = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "Привіт! Раді бачити вас в нашому телеграм-бот-магазині\n"
        "1. Кепка Basic — 200 грн\n"
        "2. Кепка Premium — 300 грн\n"
        "3. Кепка Спортивна — 400 грн\n\n"
        "Введіть номер товару, щоб розпочати замовлення."
    )
    user_states[message.chat.id] = {'step': 'waiting_for_item'}

@bot.message_handler(func=lambda message: True)
def process_message(message):
    user_id = message.chat.id
    if user_id not in user_states:
        bot.send_message(user_id, "Почніть з початку, скориставшись /start.")
        return

    user_state = user_states[user_id]

    if user_state['step'] == 'waiting_for_item':
        handle_item_selection(message, user_state)
    elif user_state['step'] == 'waiting_for_color':
        handle_color_selection(message, user_state)
    elif user_state['step'] == 'waiting_for_print':
        handle_print_selection(message, user_state)
    elif user_state['step'] == 'waiting_for_size':
        handle_size_selection(message, user_state)
    elif user_state['step'] == 'waiting_for_quantity':
        handle_quantity_selection(message, user_state)
    elif user_state['step'] == 'confirming_order':
        handle_order_confirmation(message, user_state)

def handle_item_selection(message, user_state):
    item_number = message.text.strip()

    if item_number in assortment:
        item_name, base_price = assortment[item_number]
        user_state['item'] = (item_number, item_name, base_price)
        user_state['step'] = 'waiting_for_color'

        bot.send_message(
            message.chat.id,
            f"Ви обрали {item_name}. Виберіть колір:\n"
            "1. Чорний\n2. Синій\n3. Червоний\n4. Білий"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Невірний вибір. Виберіть один з доступних номерів (1, 2 або 3)."
        )

def handle_color_selection(message, user_state):
    color_number = message.text.strip()

    if color_number in colors:
        user_state['color'] = colors[color_number]
        user_state['step'] = 'waiting_for_print'

        bot.send_message(
            message.chat.id,
            "Виберіть принт:\n"
            "1. Без принта (безкоштовно)\n"
            "2. Логотип (+50 грн)\n"
            "3. Індивідуальний дизайн (+100 грн)"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Такого кольору немає. Виберіть номер з доступних варіантів (1, 2, 3 або 4)."
        )

def handle_print_selection(message, user_state):
    print_number = message.text.strip()

    if print_number in prints:
        print_name, print_price = prints[print_number]
        user_state['print'] = (print_number, print_name, print_price)
        user_state['step'] = 'waiting_for_size'

        bot.send_message(
            message.chat.id,
            "Оберіть розмір (S, M, L, XL):"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Невірний номер принта. Виберіть номер з доступних варіантів (1, 2 або 3)."
        )

def handle_size_selection(message, user_state):
    size = message.text.strip().upper()

    if size in sizes:
        user_state['size'] = size
        user_state['step'] = 'waiting_for_quantity'

        bot.send_message(
            message.chat.id,
            "Скільки штук ви хочете замовити?"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Невірний розмір. Виберіть один з доступних (S, M, L, XL)."
        )

def handle_quantity_selection(message, user_state):
    try:
        quantity = int(message.text.strip())
        if quantity <= 0:
            bot.send_message(
                message.chat.id,
                "Будь ласка, введіть коректну кількість (ціле число більше нуля)."
            )
            return

        item_number, item_name, base_price = user_state['item']
        _, print_name, print_price = user_state['print']
        total_price = (base_price + print_price) * quantity

        user_state['quantity'] = quantity
        user_state['total_price'] = total_price
        user_state['step'] = 'confirming_order'

        bot.send_message(
            message.chat.id,
            f"Ваше замовлення:\n"
            f"Товар: {item_name}\nКолір: {user_state['color']}\nПринт: {print_name}\n"
            f"Розмір: {user_state['size']}\nКількість: {quantity}\n"
            f"Загальна вартість: {total_price} грн.\n\n"
            "Підтвердьте замовлення, відповівши 'Так', або скасуйте, відповівши 'Ні'."
        )
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Будь ласка, введіть коректну кількість (ціле число більше нуля)."
        )

def handle_order_confirmation(message, user_state):
    user_response = message.text.strip().lower()
    if user_response == 'так':
        item_number, item_name, _ = user_state['item']
        quantity = user_state['quantity']
        total_price = user_state['total_price']

        bot.send_message(
            message.chat.id,
            f"Ваше замовлення підтверджено!\n"
            f"Товар: {item_name}\nКолір: {user_state['color']}\n"
            f"Принт: {user_state['print'][1]}\nРозмір: {user_state['size']}\n"
            f"Кількість: {quantity}\nЗагальна сума: {total_price} грн.\n"
            "Дякуємо за покупку!"
        )
        del user_states[message.chat.id]
    elif user_response == 'ні':
        bot.send_message(
            message.chat.id,
            "Замовлення скасовано. Якщо ви хочете почати спочатку, введіть /start."
        )
        del user_states[message.chat.id]
    else:
        bot.send_message(message.chat.id, "Будь ласка, відповідайте 'Так' або 'Ні'.")

bot.polling(skip_pending=True)