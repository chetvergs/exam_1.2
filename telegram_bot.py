import requests
from bs4 import BeautifulSoup as BS
import telebot

TOKEN = '2131401001:AAHCthzwk6A2aQ1NovPhLKxXxlhUzQtuJao'

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

programs_url = 'https://segodnya.tv/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    'Chrome/96.0.4664.45 Safari/537.36',
    'accept': '*/*'
}

channels = ['СТС', 'Карусель', 'ТНТ', 'ТВ-3']

@bot.message_handler(commands=['start'])
def get_tv_guide(message):
    bot.send_message(
        message.chat.id
    )
@bot.message_handler(content_types=['text'])
def get_text(message):
    bot.send_message(
        message.chat.id,
        'Здравствуйте, отправьте мне команду /tv_guide'
    )

def parser(url):
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    soup = BS(response.content, 'html.parser')
    items = soup.find_all('div', class_='schedule-unit')

    channel_events = ''
    for channel in items:
        header = channel.find('a', class_='schedule-header').text
        if header in channels:
            events = channel.find_all('li')
            events_str = header + events[0].text + events[1].text + '\n'
            channel_events += events_str


    return channel_events


bot.infinity_polling()
