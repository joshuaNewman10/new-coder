from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table

class LivingSocialPipeline(object):
  """LivingSocial pipeline for storing scraped items in database"""
  def __init__(self):
    """
    Initialize database connection and sessionmaker
    Creates deals table
    """
    engine = db_connect()
    create_deals_table()
    self.Session = sessionmaker(bind=engine) #binding/connection to db with the defined engine

  def process_item(self, item, spider):
    """
    Save deals in database

    This method called for every item pipeline component
    """
    session = Self.Session() #create db session
    deal = Deals(**item) #get one scraped deal data from Deals model
    try:
      session.add(deal) #unpack an item and add to DB
      session.commit()  #before this the deal is still on the SQLALC level (commit puts it into actual db)
    except:
      session.rollback() #dont want to save partial data to db so rollback that whole item
      raise
    finally:
      session.close() #finish with closing the session
    return item