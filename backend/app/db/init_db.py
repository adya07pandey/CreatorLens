from app.db.database import (
    engine,
    Base
)

from app.db import models

Base.metadata.create_all(
    bind=engine
)

print("Tables created")