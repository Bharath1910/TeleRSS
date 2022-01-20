from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
import telebot

bot = telebot.TeleBot(
    token=TOKEN,
    parse_mode="markdown"
)

def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    markup.add(
        InlineKeyboardButton("Send RSS links", callback_data="rss")
    )

    return markup

@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "Hi...blah blah blah", reply_markup=start_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "rss":
        bot.send_message(call.message.chat.id, "Please send your RSS links one by one or seperate them with commas")
        linkList = []
        @bot.message_handler(content_types=["text"])
        def handle_links(message):
            if "," in message.text:
                links = message.text.split(",")
                for i in links:
                    linkList.append(i.strip())

            else:
                linkList.append(str(message.text))

            db = {str(message.chat.id): linkList}
            # print(db)

            # database handling: search for chat id; If not present, insert data to database else update


bot.infinity_polling()