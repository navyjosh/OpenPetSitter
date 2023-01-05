from typing import List
from openpetsitter.data_model.base import Base
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String
from typing import Optional



class User(Base, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), index=True, unique=True)    
    password_hash: Mapped[str] = mapped_column(String(128))    
    usertype: Mapped[ENUM] = mapped_column(ENUM('owner', 'sitter', name='usertype'), nullable=False)

    pets: Mapped[Optional[List['Pet']]] = relationship(
        back_populates='owner', cascade='all, delete-orphan'
    )

    jobs: Mapped[Optional[List['Job']]] = relationship('Job',
        back_populates='owner', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return self.name

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


if __name__ == '__main__':
    from openpetsitter.config import CONFIG as cfg
    from uuid import uuid1
    with cfg.session() as db:
        user = User(
            username='test_' + str(uuid1())[:10],
            usertype='owner',            
        )
        user.set_password('pwd')
        db.add(user)
        db.commit()