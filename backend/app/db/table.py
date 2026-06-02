# app/create_tables.py

from db.database import engine
from db.models import Base

Base.metadata.create_all(bind=engine)

print("Tables created")