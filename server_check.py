import telegram
from telegram.ext import Updater, MessageHandler, filters
import asyncio
import time

token = '6193827634:AAFwcTY5bqM9alfmK7LRZTbq2AF9jRyH1rc'
bot = telegram.Bot(token=token)
chat_id = 5757754313


async def main():
    await bot.sendMessage(chat_id, f"현재 시각은 {time.strftime('%Y-%m-%d %H:%M:%S')} 입니다!")

asyncio.run(main())


