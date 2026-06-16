from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
import config
from bot.handlers import router

# O'zingiz topgan proksi ma'lumotlarini shu yerga kiriting
# Format: "socks5://login:parol@ip_manzil:port"
proxy_url = "socks5://username:password@ip_address:port"

session = AiohttpSession(proxy=proxy_url)
bot = Bot(token=config.BOT_TOKEN, session=session, parse_mode=ParseMode.HTML)

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def start_bot():
    print("🤖 Telegram Bot Proksi orqali ishga tushdi...")
    await dp.start_polling(bot)