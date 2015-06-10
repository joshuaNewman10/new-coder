from sqlalchemy import create_engine
#Will allow us to map a class that defines our table structure to Postgres
#also get a function that takes our metadata of our table to make the tables we need
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime

import settings #'Take the basket'
#from settings import * 'Take everything out of the basket'

DeclarativeBase = declarative_base()

def db_connect():
  """
  Performs db connection using databse settings from settings.py
  Returns SQLAlchemy (our ORM) engine instance
  """
  # the ** unpacts all values from the Database dictionary
  #URL will map keys and values to a URL that SQLAlch can understand to make a db conneciton
  #So URL will parse out elements and make 'postgresql://Jslice@localhost:5432/scrape'
  #create_engine reads that url to eventually make connection to our DB
  return create_engine(URL(**settings.DATABASE))  

def create_deals_table(engine):
  """"""
  DeclarativeBase.metadata.create_all(engine)

class Deals(DeclarativeBase):
  """Sqlalchemy deals model"""
  __tablename__ = "deals"
  #each field will get mapped to collumn in our table when created via create_deals_table()
  id = Column(Integer, primary_key=True)
  title = Column('title', String)
  link = Column('link', String, nullable=True)
  location = Column('location', String, nullable=True)
  original_price = Column('original_price', String, nullable=True)
  price = Column('price', String, nullable=True)

