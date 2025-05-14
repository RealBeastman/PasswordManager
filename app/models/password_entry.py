from sqlalchemy import Column, Integer, String
from app.utils.db import Base

class PasswordEntry(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String)
    username = Column(String)
    password = Column(String, nullable=False) # will be encrypted