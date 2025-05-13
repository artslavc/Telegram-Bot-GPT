import telebot
from telebot import types
import threading

from g4f_engine import *

import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bot = telebot.TeleBot('TOKEN')

style = 'Подросток'

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "🍕 Спросите меня, что угодно!\n"
                                      f"Текущий Стиль: {style}")

@bot.message_handler(commands=['image'])
def handle_start(message):
    bot.send_message(message.chat.id, "📌 Какое Изображение Сгенерировать?")
    bot.register_next_step_handler(message, image_generation)


def image_generation(message):
    editable_message = bot.send_message(message.chat.id, "💤 Нейросеть Делает Картинку...")
    img_url = image_zapros(message.text)
    bot.edit_message_text('🥥 Ссылка на картинку: ' + img_url, message.chat.id, editable_message.message_id)


@bot.message_handler(commands=['chat'])
def chat_command(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton(text="🍔 Подросток")
    btn2 = telebot.types.KeyboardButton(text="🤬 Агрессивный")
    btn3 = telebot.types.KeyboardButton(text="💣 Зек")
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, "🍿 Выберите стиль общения для нейросети:", reply_markup=markup)

    bot.register_next_step_handler(message, choose_style)


def choose_style(message):
    choosed_style = message.text.split()[1]
    markup = types.ReplyKeyboardRemove()

    global style

    if choosed_style == style:
        bot.send_message(message.chat.id, '📫 У вас уже выбран этот стиль!', reply_markup=markup)
    elif choosed_style == 'Подросток':
        style = 'Подросток'
        bot.send_message(message.chat.id, '🎨 Установлен Стиль: ' + style, reply_markup=markup)
    elif choosed_style == 'Агрессивный':
        style = 'Агрессивный'
        bot.send_message(message.chat.id, '🎨 Установлен Стиль: ' + style, reply_markup=markup)
    elif choosed_style == 'Зек':
        style = 'Зек'
        bot.send_message(message.chat.id, '🎨 Установлен Стиль: ' + style, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '🚫 Я не знаю такого Стиля!')


@bot.message_handler(content_types=["text"])
def give_zapros(message):
    global style

    if message.text != '/start' and message.text != '/chat' and message.text != '/image':
        editable_message = bot.send_message(message.chat.id, "💤 Нейросеть Задумалась...")

        def thread_function():
            neiro_text = neiro_zapros(message.text, style)
            bot.edit_message_text(neiro_text, message.chat.id, editable_message.message_id)

        thread = threading.Thread(target=thread_function)
        thread.start()

bot.polling()
