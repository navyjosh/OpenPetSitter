import configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_base_path() -> Path:
    return Path(__file__).parent

CONFIG_PATH = get_base_path() / 'conf'
BASE_PATH = get_base_path()

class CFG:
    def __init__(self):
        cfp = configparser.ConfigParser()
        cfp.read(CONFIG_PATH / 'default.conf')
        cfg = cfp['dev']
        self.dbengine = create_engine(f"postgresql+pg8000://{cfg['db_user']}:{cfg['db_pwd']}@{cfg['db_host']}:{cfg['db_port']}/{cfg['db_name']}")
        self.session = sessionmaker(self.dbengine)
        self.csrf_secret = cfg['CSRF_SECRET']
    
CONFIG = CFG()