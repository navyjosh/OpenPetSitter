from openpetsitter.config import CONFIG as cfg    
from openpetsitter.data_model.base import Base
from openpetsitter.data_model.users import User
from openpetsitter.data_model.pets import Pet
from openpetsitter.data_model.jobs import Job

if __name__ == '__main__':
    Base.metadata.drop_all(cfg.dbengine)
    Base.metadata.create_all(cfg.dbengine)    