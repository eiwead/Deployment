from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):
    """
    Абстартный базовый класс, где описаны все поля и методы по умолчанию
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"# pragma: no cover

class Factory(BaseModel):
    __tablename__ = "factories"

    factory_name = Column(String, unique=True, index=True)
    factory_director = Column(String)
    factory_phone = Column(String)

    product = relationship("Product", back_populates="factory") 

 
class Product(BaseModel):
    __tablename__ = "products"

    product_name = Column(String, index=True)
    product_price = Column(Integer)
    factory_id = Column(Integer, ForeignKey("factories.id"))

    factory = relationship("Factory", back_populates="product") 
    order = relationship("Order", back_populates="product")

class Contract(BaseModel):
    __tablename__ = "contracts"
    
    client_name = Column(String, index=True)
    address = Column(String, unique=True)
    date_arrangement = Column(DateTime)
    date_execution = Column(DateTime)

    order = relationship("Order", back_populates="contract") 

class Order(BaseModel):
    __tablename__ = "orders"

    amount = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    contract_id = Column(Integer, ForeignKey("contracts.id"))

    contract = relationship("Contract", back_populates="order") 
    product = relationship("Product", back_populates="order") 