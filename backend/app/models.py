from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_coach = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    routines = relationship("Routine", back_populates="student", foreign_keys='Routine.student_id')
    payments = relationship("Payment", back_populates="student")

class Routine(Base):
    __tablename__ = "routines"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    coach_id = Column(Integer, ForeignKey("users.id"))
    day_of_week = Column(Integer) # 0=Monday, 6=Sunday
    name = Column(String)
    
    student = relationship("User", back_populates="routines", foreign_keys=[student_id])
    coach = relationship("User", foreign_keys=[coach_id])
    exercises = relationship("Exercise", back_populates="routine")

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id"))
    name = Column(String, nullable=False)
    sets = Column(Integer, default=3)
    reps = Column(Integer, default=10)
    weight = Column(Float, nullable=True) # kg/lbs
    
    routine = relationship("Routine", back_populates="exercises")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False) # 'cash' or 'transfer'
    date = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("User", back_populates="payments")
