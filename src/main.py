from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():

    db = SessionLocal() # pragma: no cover
    try:# pragma: no cover
        yield db# pragma: no cover
    finally:# pragma: no cover
        db.close()# pragma: no cover

@app.get("/factories/", response_model=list[schemas.Factory])
def read_factories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    factories = crud.get_factories(db, skip=skip, limit=limit)
    return factories

@app.get("/factories/{factory_id}", response_model=schemas.Factory)
def read_factory_by_id(factory_id: int, db: Session = Depends(get_db)):

    db_factory = crud.get_factory_by_id(db, factory_id=factory_id)
    if db_factory is None:
        raise HTTPException(status_code=404, detail="Factory not found")
    return db_factory

@app.post("/factories/{factory_id}/products/", response_model=schemas.Product)
def create_item_for_user(factory_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    
    return crud.create_factory_product(db=db, product=product, factory_id=factory_id)

@app.post("/factories/", response_model=schemas.Factory)
def create_factory(factory: schemas.FactoryCreate, db: Session = Depends(get_db)):

    db_factory = crud.get_factory_by_name(db, factory_name=factory.factory_name)
    if db_factory:
        raise HTTPException(status_code=400, detail="Factory name is already exist")
    return crud.create_factory(db=db, factory=factory)



@app.post("/products/{product_id}/orders/{contract_id}/", response_model=schemas.Order)
def create_order_for_product_contract(
    contract_id: int, product_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)
):

    return crud.create_product_order(db=db, order=order, product_id=product_id, contract_id=contract_id)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):

    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    products = crud.get_products(db, skip=skip, limit=limit)
    return products



@app.post("/contracts/", response_model=schemas.Contract)
def create_contract(contract: schemas.ContractCreate, db: Session = Depends(get_db)):

    return crud.create_contract(db=db, contract=contract)

@app.get("/contracts/", response_model=list[schemas.Contract])
def read_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    contracts = crud.get_contracts(db, skip=skip, limit=limit)
    return contracts


@app.get("/contracts/{contract_id}", response_model=schemas.Contract)
def read_contract_by_id(contract_id: int, db: Session = Depends(get_db)):

    db_contract = crud.get_contract_by_id(db, contract_id=contract_id)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract




@app.get("/orders/", response_model=list[schemas.Order])
def read_order(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):

    db_order = crud.get_order_by_id(db, order_id=order_id)# pragma: no cover
    if db_order is None:# pragma: no cover
        raise HTTPException(status_code=404, detail="Order not found")# pragma: no cover
    return db_order# pragma: no cover





