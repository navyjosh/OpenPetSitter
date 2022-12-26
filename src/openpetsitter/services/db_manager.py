from openpetsitter.data_model import Pet, PetType
from openpetsitter.config import CONFIG as cfg
from datetime import date

PET_TYPES = ['dog','cat']

PETS = {
    'rose': {'dob': date(2014,3,6), 'type':'dog'},
    'winston': {'dob':date(2020,4,16), 'type': 'dog'}
}

def delete_all_pets():
    with cfg.session() as db:
        db.query(Pet).delete()
        db.commit()

def delete_all_pet_types():
    with cfg.session() as db:
        db.query(PetType).delete()
        db.commit()

def clear_db():
    delete_all_pets()
    delete_all_pet_types()

def insert_pet_types():
    with cfg.session() as db:
        for pet in PET_TYPES:
            new_type = PetType(
                label=pet
            )
            db.add(new_type)
            db.commit()



if __name__=='__main__':
    clear_db()
    insert_pet_types()
