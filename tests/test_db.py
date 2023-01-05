from openpetsitter.data_model.base import Base
from openpetsitter.data_model.pets import Pet
from openpetsitter.data_model.users import User
from openpetsitter.data_model.jobs import Job
from openpetsitter.config import CONFIG as cfg
from datetime import date, time
from uuid import uuid1


def test_create_user():
    with cfg.session() as db:
        user = User(
            username='test_' + str(uuid1())[:10],
            usertype='owner',            
        )
        user.set_password('pwd')
        db.add(user)
        db.commit()


def test_check_password():
    with cfg.session() as db:
        user = db.query(User).filter(User.username.like('test_%')).first()
        assert user.check_password('pwd') and not user.check_password('password')


def test_create_pet():
    with cfg.session() as db:
        user = db.query(User).filter(User.username.like('test_%')).first()
        pet = Pet(
            name='test_pet',
            dob=date(2014,3,6),
            pettype='dog',
            owner=user
        )
        db.add(pet)
        db.commit()

def test_create_job():
    with cfg.session() as db:
        user = db.query(User).filter(User.username.like('test_%')).first()
        job = Job(
            owner=user,
            date=date(2022,12,30),
            scheduled_time=time(12),
            title='Walk the dogs'
        )
        db.add(job)
        db.commit()


# def test_delete_users():    
#     with cfg.session() as db:
#         users = db.query(User).filter(User.username.like('test_%')).all()
#         for u in users:
#             db.delete(u)
#         db.commit()