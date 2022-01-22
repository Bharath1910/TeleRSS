import telebot

from config import TOKEN

bot = telebot.TeleBot(
    token=TOKEN,
    parse_mode="markdown"
)


@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "text....pls do '/add'")


@bot.message_handler(content_types=['text'])
def add_links(message):
    if message.text.lower() == '/add':
        msg = bot.send_message(message.chat.id, "text...please send rss link")
        bot.register_next_step_handler(msg, handle_links)

def handle_links(message):
    db = {str(message.chat.id): [f"{message.text}"]}
    print(db)


bot.infinity_polling()