"""Here we are doing the configuration of database , so that we can access the database through python code"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


db_url = "postgresql://postgres:pritamparali@localhost:5432/Pritam" #this is the link of the db 
engine=create_engine(db_url)                    #connecting it with the db
#Now creating session to perform operations like (insert, update, delete, query data)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)    
