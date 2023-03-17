from url_cutter.db import DbClient
from url_cutter.settings import DB_CONN_STRING

db = DbClient(DB_CONN_STRING)
db.setup_db()





