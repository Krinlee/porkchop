import peewee, settings
from settings import *

db = peewee.SqliteDatabase(f"{CONFIG_DIR}/playerpoints.db")