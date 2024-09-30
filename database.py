from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///users.db"  # SQLite database

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# User model for the database
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)
    username = Column(String)
    first_name = Column(String)

# Create the database tables
Base.metadata.create_all(engine)

# Function to add a new user to the database
def add_user(telegram_id, username, first_name):
    user = User(telegram_id=telegram_id, username=username, first_name=first_name)
    session.add(user)
    session.commit()

# Function to check if user exists
def user_exists(telegram_id):
    return session.query(User).filter_by(telegram_id=telegram_id).first() is not None
