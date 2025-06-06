from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import FitnessClass, Booking
from schemas import FitnessClassOut, BookingRequest, BookingOut
from pytz import timezone
from typing import Optional
import logging


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ],
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/classes", response_model=list[FitnessClassOut])
def get_classes(
    tz: str = Query("Asia/Kolkata"),
    db: Session = Depends(get_db)
):
    try:
        client_tz = timezone(tz)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timezone")
    
    classes = db.query(FitnessClass).all()
    logger.info("Fetched class list")

    return [
        FitnessClassOut(
            id= cls.id,
            name= cls.name,
            datetime= cls.datetime.astimezone(client_tz),
            instructor= cls.instructor,
            available_slots= cls.available_slots
        )
        for cls in classes
    ]


@app.post("/book", response_model=BookingOut)
def book_class(
    booking: BookingRequest, 
    db: Session = Depends(get_db)
):
    logger.info(f"Booking attempt: {booking.client_name} ({booking.client_email}) for class ID {booking.class_id}")

    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == booking.class_id).first()

    if not fitness_class:
        logger.warning("Class not found")
        raise HTTPException(status_code=404, detail="Class not found")
    
    if fitness_class.available_slots <= 0:
        logger.warning("No slots available")
        raise HTTPException(status_code=400, detail="No slots available")
    

    new_booking = Booking(
        class_id = booking.class_id,
        client_name = booking.client_name,
        client_email = booking.client_email
    )
    db.add(new_booking)

    fitness_class.available_slots -= 1

    db.commit()
    db.refresh(new_booking)

    logger.info("Booking successful")
    return new_booking

@app.get("/bookings", response_model=list[BookingOut])
def get_bookings(
    client_email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    if client_email:
        bookings = db.query(Booking).filter(Booking.client_email == client_email).all()
        logger.info(f"Fetched bookings for email : {client_email}")
    else:
        bookings = db.query(Booking).all()
        logger.info("Fetched all bookings")

    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this email")
    
    return bookings