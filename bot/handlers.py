from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import SessionLocal
from models import Agreement
import config
from bot.keyboards import main_menu_kb, admin_menu_kb, back_kb

router = Router()

class SearchStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_contract = State()
    waiting_for_phone = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = str(message.from_user.id)
    
    if user_id == str(config.ADMIN_ID):
        await message.answer(
            "<b>Xush kelibsiz, Boss! 😎</b>\nAdmin paneli faollashdi. Amallardan birini tanlang:", 
            reply_markup=admin_menu_kb()
        )
    else:
        await message.answer(
            "<b>Kredit Magazin Botiga xush kelibsiz!</b>\n\nKreditingizni tekshirish uchun tugmani bosing:", 
            reply_markup=main_menu_kb()
        )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = str(callback.from_user.id)
    
    if user_id == str(config.ADMIN_ID):
        await callback.message.edit_text("<b>Admin Bosh Menyusi:</b>", reply_markup=admin_menu_kb())
    else:
        await callback.message.edit_text("<b>Asosiy Menyuga qaytdingiz:</b>", reply_markup=main_menu_kb())

@router.callback_query(F.data == "admin_view_all")
async def admin_view_all(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    if user_id != str(config.ADMIN_ID):
        await callback.answer("⚠️ Sizga ruxsat berilmagan!", show_alert=True)
        return
        
    db = SessionLocal()
    clients = db.query(Agreement).all()
    db.close()
    
    if not clients:
        await callback.message.edit_text("Bazada hozircha shartnomalar mavjud emas.", reply_markup=back_kb())
        return
        
    text = "📋 <b>Bot bazasidagi shartnomalar:</b>\n\n"
    for c in clients:
        text += f"📄 <code>{c.agreement_number}</code> | {c.client_name}\n💰 Qarz: {c.remaining_debt:,.0f} so'm\n\n"
        
    await callback.message.edit_text(text, reply_markup=back_kb())

@router.callback_query(F.data == "admin_status")
async def admin_status(callback: types.CallbackQuery):
    db = SessionLocal()
    count = db.query(Agreement).count()
    db.close()
    await callback.message.edit_text(f"⚙️ <b>Tizim holati:</b> AKTIV\n📊 <b>Umumiy shartnomalar soni:</b> {count} ta", reply_markup=back_kb())

@router.callback_query(F.data == "search_debt")
async def start_search(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Ism Familiyangizni kiriting:</b>\n<i>(Masalan: Abror Botirov)</i>")
    await state.set_state(SearchStates.waiting_for_name)

@router.message(SearchStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("<b>Shartnoma raqamingizni kiriting:</b>\n<i>(Masalan: SH-2024-1001)</i>")
    await state.set_state(SearchStates.waiting_for_contract)

@router.message(SearchStates.waiting_for_contract)
async def process_contract(message: types.Message, state: FSMContext):
    await state.update_data(contract=message.text)
    await message.answer("<b>Telefon raqamingizni kiriting:</b>\n<i>(Masalan: +998901234567)</i>")
    await state.set_state(SearchStates.waiting_for_phone)

@router.message(SearchStates.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = message.text.replace(" ", "")
    
    db = SessionLocal()
    agreement = db.query(Agreement).filter(
        Agreement.agreement_number == data['contract'],
        Agreement.client_name.ilike(f"%{data['name']}%"),
        Agreement.phone_number == phone
    ).first()
    
    if agreement:
        text = (
            f"👤 <b>Mijoz:</b> {agreement.client_name}\n"
            f"📄 <b>Shartnoma:</b> {agreement.agreement_number}\n"
            f"📞 <b>Tel:</b> {agreement.phone_number}\n-------------------------\n"
            f"💰 <b>Umumiy qarz:</b> {agreement.total_loan:,.0f} so'm\n"
            f"🚨 <b>Qolgan qarz:</b> {agreement.remaining_debt:,.0f} so'm\n"
            f"📅 <b>Oylik to'lov:</b> {agreement.monthly_payment:,.0f} so'm\n"
            f"📆 <b>To'lov muddati:</b> {agreement.next_payment_date}\n"
        )
        await message.answer(text, reply_markup=back_kb())
    else:
        await message.answer("❌ Bunday shartnoma topilmadi! Ma'lumotlarni tekshirib qaytadan urinib ko'ring.", reply_markup=back_kb())
        
    db.close()
    await state.clear()