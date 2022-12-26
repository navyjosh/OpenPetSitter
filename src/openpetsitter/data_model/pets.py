from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, Integer, String, ForeignKey, Column, Date, Table
from sqlalchemy.dialects.postgresql import ENUM
from datetime import date


class Base(DeclarativeBase):
    pass

class Owner(Base):
    __tablename__ = 'owner'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    
    pets: Mapped[list['Pet']] = relationship(
        back_populates='owner', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return self.name


class Pet(Base):
    __tablename__ = 'pet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    dob: Mapped[date] = mapped_column(Date)
    pettype: Mapped[ENUM] = mapped_column(ENUM('dog', 'cat', name='pettype'))
    owner_id: Mapped[int] = mapped_column(ForeignKey('owner.id'))

    owner = relationship('Owner', back_populates='pets')    


    def __repr__(self):
        return self.name

    @property
    def calculate_age():
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


if __name__ == '__main__':    
    from openpetsitter.config import CONFIG as cfg    
    Base.metadata.drop_all(cfg.dbengine)
    Base.metadata.create_all(cfg.dbengine)    