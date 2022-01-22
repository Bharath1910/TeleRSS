import telebot
import psycopg2

from config import TOKEN, DBU, DBU, DBP, DBH

bot = telebot.TeleBot(
    token=TOKEN,
    parse_mode="markdown"
)

conn = psycopg2.connect(
    database=DBN,
    user=DBU,
    password=DBP,
    host=DBH,
    port=DBP
    )

cur = conn.cursor()

@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "text....pls do '/add'")


@bot.message_handler(commands=['add'])
def message_handler(message):
    msg = bot.send_message(message.chat.id, "text...please send rss link")
    bot.register_next_step_handler(msg, handle_links)

def handle_links(message):
    cur.execute("SELECT rss_links FROM links WHERE chat_id=%s", (message.chat.id, ))
    result = cur.fetchone()
    if result is not None:
        links = eval(result[0])
        links.append(message.text)
        cur.execute("UPDATE links SET rss_links=%s WHERE chat_id=%s", (f"{links}", message.chat.id))
        conn.commit()
    elif result is None:
        cur.execute("INSERT INTO links VALUES(%s, %s)", (message.chat.id, f"['{message.text}']"))
        conn.commit()
    


bot.infinity_polling()