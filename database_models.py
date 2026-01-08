from sqlalchemy import Column,Integer,Float,String 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class product(Base):
    __tablename__ = "product"           #this is used for giving table name ! 
    id = Column(Integer, primary_key=True,index=True)           
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
