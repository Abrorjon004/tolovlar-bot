import datetime
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime
from database import Base, engine, SessionLocal

class Agreement(Base):
    __tablename__ = 'agreements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agreement_number = Column(String(50), unique=True, nullable=False, index=True)
    client_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False, index=True)
    total_loan = Column(Numeric, nullable=False)
    remaining_debt = Column(Numeric, nullable=False)
    monthly_payment = Column(Numeric, nullable=False)
    next_payment_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Demo uchun birinchi mijozni qo'shib qo'yamiz
    db = SessionLocal()
    if not db.query(Agreement).first():
        demo = Agreement(
            agreement_number="SH-2024-1001",
            client_name="Abror Botirov",
            phone_number="+998901234567",
            total_loan=2800000.00,
            remaining_debt=2450000.00,
            monthly_payment=350000.00,
            next_payment_date=datetime.date(2026, 6, 15)
        )
        db.add(demo)
        db.commit()
    db.close()