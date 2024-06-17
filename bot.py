import os, datetime
import telebot
from dotenv import load_dotenv, find_dotenv
import yfinance as yf

load_dotenv(find_dotenv())
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to slumbot! Type /wagwan to be greeted properly.")

@bot.message_handler(commands=['wagwan'])
def send_info(message):
    bot.reply_to(message, "Bomboclaat! Wagwan mi likkle yute? Holla if you tryna bun up, mon. One love!")

def majors_ohlc_today():
    interval = "1d"
    df_btc = yf.download('BTC-USD', interval=interval, start=datetime.date.today().strftime("%Y-%m-%d"))
    df_eth = yf.download('ETH-USD', interval=interval, start=datetime.date.today().strftime("%Y-%m-%d"))
    today_string = datetime.date.today().strftime("%Y/%m/%d")
    btc_data_today = df_btc.loc[today_string]
    eth_data_today = df_eth.loc[today_string]
    return today_string, btc_data_today, eth_data_today

def build_majors_message_today():
    today_string, btc_data_today, eth_data_today = majors_ohlc_today()
    title = "Crypto Majors 1D Summary\n{}\n".format(today_string)
    btc_close = round(btc_data_today['Adj Close'],1)
    btc_change = round(((btc_data_today['Adj Close']/btc_data_today['Open'])-1)*100,2)
    eth_close = round(eth_data_today['Adj Close'],2)
    eth_change = round(((eth_data_today['Adj Close']/eth_data_today['Open'])-1)*100,2)
    btc_summary = "{}/{}: {} ({:.2f}%)".format('BTC','USD',btc_close,btc_change)
    eth_summary = "{}/{}: {} ({:.2f}%)".format('ETH','USD',eth_close,eth_change)
    ethbtc_close = round(eth_data_today['Adj Close']/btc_data_today['Adj Close'],5)
    ethbtc_change = round((((eth_data_today['Adj Close']/btc_data_today['Adj Close'])/(eth_data_today['Open']/btc_data_today['Open']))-1)*100,2)
    ethbtc_summary = "{}/{}: {} ({:.2f}%)".format('ETH','BTC',ethbtc_close,ethbtc_change)
    majors_message = "{}\n{}\n{}\n\n{}".format(title,btc_summary,eth_summary,ethbtc_summary)
    return majors_message

@bot.message_handler(commands=['majors'])
def send_info(message):
    majors_message = build_majors_message_today()
    bot.reply_to(message, majors_message)

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "invalid command, likkle yute")

# Start the bot
bot.polling()
