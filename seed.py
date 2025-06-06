from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import engine, SessionLocal,Base
from models import FitnessClass
import pytz

IST = pytz.timezone("Asia/Kolkata")

Base.metadata.create_all(bind=engine)


sample_classes = [
    FitnessClass(
        name = "Yoga",
        datetime=IST.localize(datetime(2025,6,4,10,0)),
        instructor = "Siri",
        available_slots = 10
    ),
    FitnessClass(
        name = "Zumba",
        datetime=IST.localize(datetime(2025,6,4,12,0)),
        instructor="Ajay",
        available_slots = 8
    ),
    FitnessClass(
        name = "HIIT",
        datetime=IST.localize(datetime(2025,6,4,17,0)),
        instructor="Bharath",
        available_slots = 8
    )
]

db:Session = SessionLocal()

db.query(FitnessClass).delete()
for cls in sample_classes:
    db.add(cls)
db.commit()
db.close()

print("Seeded data with IST timezone.")