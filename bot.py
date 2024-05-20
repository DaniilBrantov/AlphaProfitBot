import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Считываем данные из JSON-файла
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Инициализация бота
bot = telebot.TeleBot(config["telegram_api_key"])

with open("messages.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Функция для создания клавиатуры, если есть кнопки
def create_keyboard(buttons):
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        if "callback_data" in button:
            keyboard.add(InlineKeyboardButton(button["text"], callback_data=button["callback_data"]))
        elif "url" in button:
            keyboard.add(InlineKeyboardButton(button["text"], url=button["url"]))
    return keyboard

# Функция для отправки сообщения с возможной клавиатурой
def send_message_with_buttons(chat_id, data_key, name=""):
    message_data = data.get(data_key, {})
    text = message_data.get("text", "").format(name=name)
    image_url = message_data.get("image_url", "")
    buttons = message_data.get("buttons", [])
    
    keyboard = create_keyboard(buttons) if buttons else None
    
    if image_url:
        bot.send_photo(chat_id, open(image_url, 'rb'), caption=text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, text, reply_markup=keyboard)

# Обработка команды "/start"
@bot.message_handler(commands=["start"])
def start_handler(message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    send_message_with_buttons(message.chat.id, "start_message", name=name)
    notify_admins(user_id, name)

# Уведомление администраторов о новом пользователе
def notify_admins(user_id, name):
    for admin_id in config["admin_ids"]:
        bot.send_message(admin_id, f"Новый пользователь начал взаимодействие с ботом:\nИмя: {name}\nID: {user_id}")

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    send_message_with_buttons(call.message.chat.id, call.data, name=call.from_user.first_name)

# Запуск бота
bot.polling()
