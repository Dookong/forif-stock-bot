import telegram
import asyncio
import helper.commons as commons

class MessageSender:
    keys = commons.get_telegram_keys()
    chat_id = keys[0]
    token = keys[1]
    bot = telegram.Bot(token=token)
    
    async def aynsc_send(self, message):
        await self.bot.sendMessage(self.chat_id, message)

    def send(self, message):
        asyncio.run(self.aynsc_send(message))