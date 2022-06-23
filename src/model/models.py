import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine('mysql+pymysql://root:secret@authmariadb:3306/authdb?charset=utf8mb4')
Base = declarative_base();

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
       
class Token(Base):
    __tablename__ = 'token'
    email = Column(String(50), primary_key=True, nullable=False)
    token = Column(String(256), nullable=False)
    timestamp = Column(Integer, nullable=False)

    def __init__(self, email, token, timestamp):
        self.email = email
        self.token = token
        self.timestamp = timestamp

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}