from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

# We'll use Alembic for migrations instead of create_all
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gymbro API")

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create(db=db, obj_in=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@app.post("/routines/", response_model=schemas.Routine)
def create_routine(routine: schemas.RoutineCreate, db: Session = Depends(get_db)):
    return crud.routine.create(db=db, obj_in=routine)

@app.get("/routines/student/{student_id}", response_model=List[schemas.Routine])
def read_routines_for_student(student_id: int, db: Session = Depends(get_db)):
    routines = crud.routine.get_by_student(db, student_id=student_id)
    return routines

@app.post("/payments/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.payment.create(db=db, obj_in=payment)

@app.get("/payments/", response_model=List[schemas.Payment])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.payment.get_multi(db, skip=skip, limit=limit)
