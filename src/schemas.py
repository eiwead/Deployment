from pydantic import BaseModel
from datetime import date
class OrderBase(BaseModel):

    amount: int


class OrderCreate(OrderBase):

    pass

class Order(OrderBase):

    id: int
    product_id: int
    contract_id: int

    class Config:
        orm_mode = True




class ProductBase(BaseModel):

    product_name: str
    product_price: int
    


class ProductCreate(ProductBase):

    pass


class Product(ProductBase):

    id: int
    factory_id: int
    order: list[Order] = []

    class Config:
        orm_mode = True

class FactoryBase(BaseModel):

    factory_name: str
    factory_director: str 
    factory_phone: str


class FactoryCreate(FactoryBase):

    pass


class Factory(FactoryBase):

    id: int
    product: list[Product] = []


    class Config:

        orm_mode = True




class ContractBase(BaseModel):

    client_name: str
    address: str
    date_arrangement: date
    date_execution: date

class ContractCreate(ContractBase):

    pass

class Contract(ContractBase):

    id: int
    order: list[Order] = []

    class Config:
        orm_mode = True



