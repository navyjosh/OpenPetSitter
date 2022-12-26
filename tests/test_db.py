from openpetsitter.data_model.pets import Pet, Owner
from openpetsitter.config import CONFIG as cfg
from datetime import date

PET_TYPES = ['dog','cat']

PETS = {
    'rose': {'dob': date(2014,3,6), 'type':'dog'},
    'winston': {'dob': date(2020,4,16), 'type': 'dog'}
}

def test_create_owner():
    with cfg.session() as db:
        josh = Owner(
            name='Josh',
        )
        db.add(josh)
        db.commit()

def test_create_pet():
    with cfg.session() as db:
        owner = db.query(Owner).first()
        rose = PETS['rose']
        pet = Pet(
            name='Rose',
            dob=rose['dob'],
            pettype='dog',
            owner=owner
        )
        db.add(pet)
        db.commit()