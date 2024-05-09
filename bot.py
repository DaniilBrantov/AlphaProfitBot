import telebot
import json
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# "video1_done": {
#         "text": "ВИДЕО №2\nКак заработать первые 100 000₽ абсолютно без финансовых вложений в первый же месяц?\nЯ зашёл в проект в середине марта. За 2 недели команда принесла более 30 000₽ пассивного дохода.\n\nПросто представь, какой пассивный доход будет в апреле, когда включится хотя бы 20 человек из 100.\n\nПосле просмотра второго видео, ты узнаешь:\n- Как заработать 100 000₽ абсолютно без финансовых вложений\n- Как создать источник пассивного дохода от 30 000₽ в первый же месяц\n- Как собирать свою команду и не тратить время на их обучение\n! Только не откладывай просмотр на потом - видео доступно только 24 часа.",
#         "image_url": "",
#         "buttons": [
#             {"text": "Открыть видео", "callback_data": "video2_open"}
#         ]
#     }



# Инициализация бота
bot = telebot.TeleBot("6901437597:AAFb4uklsoGq5OdIAhPs3rl1xNXDvrrBO84")

# Считываем данные из JSON-файла
with open("messages.json", "r") as file:
    data = json.load(file)

# Функция для создания клавиатуры, если есть кнопки
def create_keyboard(data_key):
    if "buttons" not in data[data_key]:
        return None
    
    keyboard = InlineKeyboardMarkup()
    for button in data[data_key]["buttons"]:
        if "callback_data" in button:
            keyboard.add(InlineKeyboardButton(button["text"], callback_data=button["callback_data"]))
        elif "url" in button:
            keyboard.add(InlineKeyboardButton(button["text"], url=button["url"]))
        else:
            keyboard.add(InlineKeyboardButton(button["text"], callback_data="default_action"))
    
    return keyboard

# Функция для отправки сообщения с возможной клавиатурой
def send_message_with_buttons(chat_id, data_key):
    keyboard = create_keyboard(data_key)

    if "image_url" in data[data_key]:
        # Отправка фотографии, если есть image_url
        bot.send_photo(chat_id, open(data[data_key]["image_url"], 'rb'), data[data_key]["text"], reply_markup=keyboard)
    else:
        # Отправка текста, если нет фотографии
        bot.send_message(chat_id, data[data_key]["text"], reply_markup=keyboard if keyboard else None)

# Обработка команды "/start"
@bot.message_handler(commands=["start"])
def start_handler(message):
    chat_id = message.chat.id
    send_message_with_buttons(chat_id, "start_message")
    # time.sleep(30)  # Через 30 секунд отправляем первый видеоблок
    # send_message_with_buttons(chat_id, "video1")

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    callback_data = call.data

    # Карта действий на основе callback_data
    callback_actions = {
        "video1": "video1",
        "video3_done": "video3_done",
    }

    if callback_data in callback_actions:
        send_message_with_buttons(chat_id, callback_actions[callback_data])

# Запуск бота
bot.polling()
