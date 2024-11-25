import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command

# Токен вашого Telegram-бота
API_TOKEN = '7676689297:AAFwrBZlmlMg0EFdSuKKBalC8aM3qOt5Jzk'

# Створюємо об'єкти бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Фіктивна база даних для кепок
catalog = [
    {"id": 1, "name": "Спортивна кепка", "price": 1000, "description": "Ідеально для пробіжок."},
    {"id": 2, "name": "Класична кепка", "price": 1200, "description": "Елегантний стиль."},
    {"id": 3, "name": "Кепка унісекс", "price": 1500, "description": "Підходить для всіх."}
]

# Кошик користувача
user_cart = {}

# Головне меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог")],
        [KeyboardButton(text="Кошик")],
        [KeyboardButton(text="Оформити замовлення")]
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привіт! Ласкаво просимо до нашого магазину кепок. Оберіть дію з меню нижче.",
        reply_markup=main_menu
    )

# Перегляд каталогу
@dp.message(lambda message: message.text == "Каталог")
async def show_catalog(message: Message):
    catalog_text = "Ось наш каталог кепок:\n\n"
    for item in catalog:
        catalog_text += f"🧢 {item['name']}\nЦіна: {item['price']}₴\n{item['description']}\n\n"
    catalog_text += "Введіть номер товару, щоб додати його до кошика."
    await message.answer(catalog_text)

# Додавання товару до кошика
@dp.message(lambda message: message.text.isdigit())
async def add_to_cart(message: Message):
    product_id = int(message.text)
    product = next((item for item in catalog if item["id"] == product_id), None)
    if product:
        user_cart.setdefault(message.from_user.id, []).append(product)
        await message.answer(f"🛒 {product['name']} додано до кошика!")
    else:
        await message.answer("Такого товару немає в каталозі.")

# Перегляд кошика
@dp.message(lambda message: message.text == "Кошик")
async def show_cart(message: Message):
    cart = user_cart.get(message.from_user.id, [])
    if cart:
        cart_text = "🛒 Ваш кошик:\n\n"
        total = 0
        for item in cart:
            cart_text += f"{item['name']} - {item['price']}₴\n"
            total += item['price']
        cart_text += f"\nРазом: {total}₴"
        await message.answer(cart_text)
    else:
        await message.answer("Ваш кошик порожній.")

# Оформлення замовлення
@dp.message(lambda message: message.text == "Оформити замовлення")
async def checkout(message: Message):
    cart = user_cart.get(message.from_user.id, [])
    if cart:
        await message.answer(
            "Дякуємо за ваше замовлення! Ми зв'яжемося з вами для уточнення деталей доставки.",
            reply_markup=main_menu
        )
        user_cart[message.from_user.id] = []  # Очищення кошика
    else:
        await message.answer("Ваш кошик порожній. Додайте товари перед оформленням замовлення.")

# Обробка інших повідомлень
@dp.message()
async def handle_unknown(message: Message):
    await message.answer("Будь ласка, оберіть дію з меню.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
