from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

db_path = os.path.join(os.path.dirname(__file__),"..", "data", 'passwords.db')
engine = create_engine(f"sqlite:///{db_path}", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()