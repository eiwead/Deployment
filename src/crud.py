from sqlalchemy.orm import Session

from src import models, schemas

def create_factory(db: Session, factory: schemas.FactoryCreate):

    db_factory = models.Factory(**factory.dict()) 
    db.add(db_factory)
    db.commit()
    db.refresh(db_factory)
    return db_factory



def create_contract(db: Session, contract: schemas.ContractCreate):

    db_contract = models.Contract(client_name=contract.client_name, address=contract.address, date_arrangement=contract.date_arrangement, date_execution=contract.date_execution)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def create_factory_product(db: Session, product: schemas.ProductCreate, factory_id: int):
 
    db_product = models.Product(**product.dict(), factory_id=factory_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_product_order(db: Session, order: schemas.OrderCreate, product_id: int, contract_id: int):

    db_order = models.Order(**order.dict(), product_id=product_id, contract_id=contract_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_factory_by_id(db: Session, factory_id: int):

    return db.query(models.Factory).filter(models.Factory.id == factory_id).first()

def get_order_by_id(db: Session, order_id: int):

    return db.query(models.Order).filter(models.Order.id == order_id).first() # pragma: no cover

def get_contract_by_id(db: Session, contract_id: int):
 
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()




def get_factory_by_name(db: Session, factory_name: str):
    return db.query(models.Factory).filter(models.Factory.factory_name == factory_name).first()




def get_products(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Product).offset(skip).limit(limit).all()

def get_orders(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Order).offset(skip).limit(limit).all()

def get_contracts(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Contract).offset(skip).limit(limit).all()

def get_factories(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Factory).offset(skip).limit(limit).all()