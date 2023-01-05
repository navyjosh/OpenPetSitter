from openpetsitter.data_model.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import create_engine, Integer, String, ForeignKey, Column, Date, Table, TypeDecorator, TypeDecorator
from sqlalchemy.dialects.postgresql import ENUM
from datetime import date


class Pet(Base):
    __tablename__ = 'pet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    dob: Mapped[date] = mapped_column(Date)
    pettype: Mapped[ENUM] = mapped_column(ENUM('dog', 'cat', name='pettype'))
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    owner = relationship('User', back_populates='pets')

    def __repr__(self):
        return self.name

    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
