import peewee, settings
from settings import *

db = peewee.SqliteDatabase(f"{ASSET_DIR}/playerpoints.db")