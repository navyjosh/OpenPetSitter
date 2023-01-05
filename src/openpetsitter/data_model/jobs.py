from typing import List, Optional
from openpetsitter.data_model.base import Base
from openpetsitter.data_model.pets import Pet
from openpetsitter.data_model.users import User
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Date, Time, String
from sqlalchemy.dialects.postgresql import ENUM
import datetime as dt


class Sitter(Base):
    __tablename__ = 'sitter'
    id: Mapped[int] = mapped_column(primary_key=True)

    accepted_jobs: Mapped[Optional[List['Job']]] = relationship(
        back_populates='sitter'
    )


class Job(Base):
    __tablename__ = 'job'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    sitter_id: Mapped[int] = mapped_column(ForeignKey('sitter.id'), nullable=True)
    pet_id: Mapped[Optional[List['Pet']]] = mapped_column(ForeignKey('pet.id'), nullable=True)
    start_time: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)
    stop_time: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)
    date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    scheduled_time: Mapped[dt.time] = mapped_column(Time, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    owner = relationship('User', back_populates='jobs')
    sitter = relationship('Sitter', back_populates='accepted_jobs')
    pets: Mapped[Optional[list['Pet']]] = relationship('Pet')

