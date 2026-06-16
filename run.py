import threading
import asyncio
from models import init_db
from bot.main_bot import start_bot
from admin_panel import run_admin_panel

def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())

if __name__ == "__main__":
    # 1. Bazani avtomat yaratish va tekshirish
    init_db()
    
    # 2. Botni fonda (Thread ichida) yoqish
    bot_thread = threading.Thread(target=start_bot_thread)
    bot_thread.daemon = True
    bot_thread.start()
    
    # 3. Asosiy terminal admin panelini yurgizish
    run_admin_panel()