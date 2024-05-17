from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
