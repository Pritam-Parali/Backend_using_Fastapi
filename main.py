from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware      #importing cors middleware  
from models import product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)       #this line will create the table for us
#performing CRUD operation

@app.get('/')
def greet():
    return "This is the code written in backend"

#List elements
products=[
    product(id=1,name="Mobile",description="Realme flagship phone",price=42000.99,quantity=1),
    product(id=2,name="Laptop",description="Lenovo laptop",price=40000,quantity=2),
    product(id=3,name="table",description="Wooden table",price=2000,quantity=10),
    product(id=4,name="Sports Bike",description="KTM RC 200",price=40000,quantity=20)
]


#Here we will create a function so that we dont have to  write db=session() in every function later
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

#we have written this function to avoid dupliacte data insertion. 
def init_db():
    db=session()
    count = db.query(database_models.product).count()
    if count==0:
        for product in products:
            db.add(database_models.product(**product.model_dump()))
        db.commit()

init_db()

@app.get('/products')
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.product).all() # its a query to fetch all the elements 
    return db_products
    

#Now fetching the details by id 
@app.get('/products/{id}')
def fetch_by_id(id: int , db:Session = Depends(get_db) ):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        return db_product
    return "product not found"

#Now doing post request means sending request

@app.post('/products')
def add_product(product:product,db:Session = Depends(get_db)):
    db.add(database_models.product(**product.model_dump()))
    db.commit()
    return product

#Now Updating the details of the product using put api calling

@app.put('/products/{id}')
def update_product(id: int,product : product,db:Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product added successfully"
    else:
        return "Nothing to add"   

#Alternate way

# def update_product(id:int , product:product):
#     for index,i in enumerate(products):
#         if i.id == id:
#             products[index]=product
#             return "product added"
#     return "Nothing to add"



#Now performing delete 
@app.delete('/products/{id}')
def delete_product(id: int,db:Session = Depends(get_db)):
        db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
        return "Nothing found to delete !!" 