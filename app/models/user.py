from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index, UniqueConstraint, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.schemas.enum import Gender
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255))
    mobile_number = Column(String, nullable=False)
    email = Column(String(255))
    national_code = Column(String(255))
    gender = Column(Enum(Gender), nullable=False)
    profile_image = Column(String(36))
    is_active = Column(Boolean, nullable=False)
    loginable = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean, default=False)
    mobile_visible = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True)


    __table_args__ = (
        UniqueConstraint('mobile_number', 'email', name='uniques'),
        Index('index', 'name', 'mobile_number', 'email'),
    )