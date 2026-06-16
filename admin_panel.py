import os
import crud

def run_admin_panel():
    while True:
        print("\n" + "="*50)
        print("🛠 KREDIT TIZIMI - PROFESSIONAL TERMINAL ADMIN PANEL")
        print("="*50)
        print("1. 📋 Barcha shartnomalarni ko'rish")
        print("2. ➕ Yangi shartnoma qo'shish")
        print("3. ✏️ Shartnoma ma'lumotlarini o'zgartirish")
        print("4. 🗑 Shartnomani o'chirib yuborish")
        print("5. ❌ Chiqish")
        print("="*50)
        
        choice = input("Tanlovingizni kiriting (1-5): ")
        
        if choice == "1":
            clients = crud.get_all_clients()
            print("\n📋 BAZADAGI BARCHA MIJOZLAR RO'YXATI:")
            print("-" * 80)
            for c in clients:
                print(f"Doc: {c.agreement_number} | {c.client_name} | Tel: {c.phone_number} | Qarz: {c.remaining_debt:,.0f} so'm | Muddat: {c.next_payment_date}")
            print("-" * 80)
            
        elif choice == "2":
            print("\nYANGI SHARTNOMA QO'SHISH:")
            num = input("Shartnoma raqami (e.g., SH-2024-1002): ")
            name = input("Ism Familiya: ")
            phone = input("Tel (e.g., +998901234567): ").replace(" ", "")
            total = input("Umumiy qarz summasi: ")
            rem = input("Qolgan qarz summasi: ")
            month = input("Oylik to'lov summasi: ")
            date_str = input("Keyingi to'lov sanasi (YIL-OY-KUN, masalan: 2026-06-15): ")
            
            res = crud.add_client(num, name, phone, total, rem, month, date_str)
            print(res)
            
        elif choice == "3":
            print("\nSHARTNOMANI TAHRIRLASH:")
            num = input("O'zgartirilishi kerak bo'lgan shartnoma raqami: ")
            print("Nimani o'zgartirmoqchisiz? (ism / tel / qarz / oylik / sana)")
            field = input("Tanlov: ").lower()
            new_val = input("Yangi qiymat: ")
            
            res = crud.update_client(num, field, new_val)
            print(res)
            
        elif choice == "4":
            print("\n🚨 SHARTNOMANI O'CHIRISH:")
            num = input("O'chirib yubormoqchi bo'lgan shartnoma raqamingiz: ")
            confirm = input(f"Rostdan ham {num} shartnomani butunlay o'chirmoqchimisiz? (ha/yo'q): ")
            if confirm.lower() == 'ha':
                res = crud.delete_client(num)
                print(res)
            else:
                print("❌ O'chirish bekor qilindi.")
                
        elif choice == "5":
            print("👋 Admin panel yopildi.")
            os._exit(0)