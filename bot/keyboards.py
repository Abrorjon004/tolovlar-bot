from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Grafik to'lovni to'lash", callback_query_data="search_debt")],
        [InlineKeyboardButton(text="⚡ Muddatdan avval to'lash", callback_query_data="search_debt")],
        [InlineKeyboardButton(text="🔍 Qarzimni ko'rish", callback_query_data="search_debt")]
    ])

def admin_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Barcha shartnomalar (Botda)", callback_query_data="admin_view_all")],
        [InlineKeyboardButton(text="🔍 Mijoz qidirish / Tekshirish", callback_query_data="search_debt")],
        [InlineKeyboardButton(text="⚙️ Tizim holati", callback_query_data="admin_status")]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_query_data="back_to_main")]
    ])