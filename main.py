from config import *
import telebot, psycopg2
import feedparser
import re

# Telegram API setup
bot = telebot.TeleBot(
    token=TOKEN,
    parse_mode="markdown"
)

# Database connection and setup
conn = psycopg2.connect(
    database=DB_Name,user=DB_User,
    password=DB_Password,host=DB_Host,
    port=DB_Port # Defaut port is 5432, use 5432 if you are not sure about it
    )

cur = conn.cursor()


def feed_details(url):
    """
    Accepts a string which should be a RSS feed,
    then it parses the link and sends the
    title, link and description of the feed.
    """
    link = feedparser.parse(url.text)
    details =  {
        "title":link.feed.title,
        "link":link.feed.link,
        "description":link.feed.description
        }
    bot.send_message(url.chat.id, f"Title: {details['title']}\nLink: {details['link']}\nDescription: {details['description']}")


@bot.message_handler(commands=['start','help'])
def command_start(message):
    # Doc strings looks nice tbh
    help_text = """
Hey! This is a RSS Feed Bot.

- /add to add a RSS link.
- /help to see this message again.
- /list to see all your registered RSS links.
    """
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['add'])
def command_add(message):
    msg = bot.send_message(message.chat.id, "Send a RSS feed link.")
    bot.register_next_step_handler(msg, handle_links)

def handle_links(message):
    regex=("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" + "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
    if re.search(re.compile(regex), message.text):
        cur.execute("SELECT rss_links FROM links WHERE chat_id=%s", (message.chat.id,))
        result = cur.fetchone()

        if result is not None:
            links = eval(result[0])
            links.append(message.text)
            cur.execute("UPDATE links SET rss_links=%s WHERE chat_id=%s", (f"{links}", message.chat.id))
            conn.commit()

        elif result is None:
            cur.execute("INSERT INTO links VALUES(%s, %s)", (message.chat.id, f"['{message.text}']"))
            conn.commit()

        feed_details(message)
    else:
        bot.send_message(message.chat.id, "Please send a valid url.")

@bot.message_handler(commands=['list'])
def command_list(message):
    cur.execute("SELECT rss_links FROM links WHERE chat_id=%s", (message.chat.id,))
    result = cur.fetchone()
    
    if result is not None:
        text=""
        for i in eval(result[0]):
            text += f"{(feedparser.parse(i)).feed.title} | {i}\n"
        bot.send_message(message.chat.id, f"{text}")

    elif result is None:
        bot.send_message(message.chat.id, "Nothing to list. Use '/add' to add one.")

bot.infinity_polling()