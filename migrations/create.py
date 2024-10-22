from sqlalchemy import create_engine
from storage.db import DB_CONNECTION_STRING
from app.models import Base

engine = create_engine(DB_CONNECTION_STRING)
Base.metadata.create_all(engine)