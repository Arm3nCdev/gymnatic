from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, schemas
from .database import engine, get_db
from .auth import (
    verify_password,
    create_access_token,
    get_current_user,
    create_refresh_token,
    get_refresh_token_expiration,
)

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
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.user.create(db=db, obj_in=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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
def create_routine(routine: schemas.RoutineCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.routine.create(db=db, obj_in=routine)


@app.get("/routines/student/{student_id}", response_model=List[schemas.Routine])
def read_routines_for_student(student_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    routines = crud.routine.get_by_student(db, student_id=student_id)
    return routines


@app.post("/payments/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.payment.create(db=db, obj_in=payment)


@app.get("/payments/", response_model=List[schemas.Payment])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.payment.get_multi(db, skip=skip, limit=limit)


@app.post("/auth/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
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

    refresh_token = create_refresh_token()

    crud.refresh_token.create(
        db,
        user_id=db_user.id,
        token=refresh_token,
        expires_at=get_refresh_token_expiration(),
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post("/auth/refresh", response_model=schemas.Token)
def refresh_access_token(
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing",
        )

    db_refresh_token = crud.refresh_token.get_valid(
        db,
        token=refresh_token,
    )

    if not db_refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    access_token = create_access_token(
        data={
            "sub": str(db_refresh_token.user_id),
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post("/auth/logout")
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if refresh_token:
        db_refresh_token = crud.refresh_token.get_by_token(
            db,
            token=refresh_token,
        )

        if db_refresh_token:
            crud.refresh_token.revoke(
                db,
                refresh_token=db_refresh_token,
            )

    response.delete_cookie(
        key="refresh_token",
    )

    return {"message": "Sesión cerrada correctamente"}
