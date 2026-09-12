from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime

class ExerciseBase(BaseModel):
    name: str
    sets: int = 3
    reps: int = 10
    weight: Optional[float] = None

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    routine_id: int

class RoutineBase(BaseModel):
    day_of_week: int
    name: str

class RoutineCreate(RoutineBase):
    student_id: int
    coach_id: int

class Routine(RoutineBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    coach_id: int
    exercises: List[Exercise] = []

class PaymentBase(BaseModel):
    amount: float
    payment_method: str

class PaymentCreate(PaymentBase):
    student_id: int

class Payment(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    date: datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_coach: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str