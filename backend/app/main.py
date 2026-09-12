from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, schemas
from .database import engine, get_db
from .auth import verify_password, create_access_token

# We'll use Alembic for migrations instead of create_all
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gymbro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.user.get(db, id=user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    crud.user.remove(db, id=user_id)

    return {"message": "User deleted successfully"}

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

@app.post("/auth/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.user.get_by_email(db, email=user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "is_coach": db_user.is_coach,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }