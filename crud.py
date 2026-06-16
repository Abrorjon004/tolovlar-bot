import datetime
from database import SessionLocal
from models import Agreement

def add_client(agreement_num, name, phone, total, remaining, monthly, date_str):
    db = SessionLocal()
    try:
        y, m, d = map(int, date_str.split('-'))
        new_client = Agreement(
            agreement_number=agreement_num,
            client_name=name,
            phone_number=phone,
            total_loan=float(total),
            remaining_debt=float(remaining),
            monthly_payment=float(monthly),
            next_payment_date=datetime.date(y, m, d)
        )
        db.add(new_client)
        db.commit()
        return "✅ Mijoz muvaffaqiyatli qo'shildi!"
    except Exception as e:
        db.rollback()
        return f"❌ Xatolik yuz berdi: {e}"
    finally:
        db.close()

def get_all_clients():
    db = SessionLocal()
    clients = db.query(Agreement).all()
    db.close()
    return clients

def update_client(agreement_num, field, new_value):
    db = SessionLocal()
    client = db.query(Agreement).filter(Agreement.agreement_number == agreement_num).first()
    if not client:
        db.close()
        return "❌ Bunday shartnoma raqami topilmadi!"
    try:
        if field == "ism": client.client_name = new_value
        elif field == "tel": client.phone_number = new_value
        elif field == "qarz": client.remaining_debt = float(new_value)
        elif field == "oylik": client.monthly_payment = float(new_value)
        elif field == "sana":
            y, m, d = map(int, new_value.split('-'))
            client.next_payment_date = datetime.date(y, m, d)
        db.commit()
        return "✅ Mijoz ma'lumotlari muvaffaqiyatli o'zgartirildi!"
    except Exception as e:
        db.rollback()
        return f"❌ Xatolik: {e}"
    finally:
        db.close()

def delete_client(agreement_num):
    db = SessionLocal()
    client = db.query(Agreement).filter(Agreement.agreement_number == agreement_num).first()
    if not client:
        db.close()
        return "❌ Bunday shartnoma raqami topilmadi!"
    try:
        db.delete(client)
        db.commit()
        return "🗑 Shartnoma bazadan butunlay o'chirib yuborildi!"
    except Exception as e:
        db.rollback()
        return f"❌ Xatolik: {e}"
    finally:
        db.close()