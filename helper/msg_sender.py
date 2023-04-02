import telegram
import asyncio

token = '6193827634:AAFwcTY5bqM9alfmK7LRZTbq2AF9jRyH1rc'
bot = telegram.Bot(token=token)
chat_id = 5757754313

async def send(msg):
    await bot.sendMessage(chat_id, msg)

def send_msg(msg):
    asyncio.run(send(msg))