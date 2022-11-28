from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_base.db"  # Тестовая БД

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_create_factory():
    response = client.post(
        "/factories/",
        json={"factory_name": "testing", "factory_director": "Human", "factory_phone" : "111-111"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["factory_name"] == "testing"

def test_create_exist_factory():
    response = client.post(
        "/factories/",
        json={"factory_name": "testing", "factory_director": "Human", "factory_phone" : "111-111"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Factory name is already exist"

def test_read_factories():
    response = client.get("/factories/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["factory_name"] == "testing"

def test_get_factory_by_id():
    response = client.get("/factories/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["factory_name"] == "testing"

def test_factory_not_found():
    response = client.get("/factories/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Factory not found"

def test_add_product_to_factory():
    response = client.post(
        "/factories/1/products/",
        json={"product_name": "Тестовая бумага", "product_price": 100}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "Тестовая бумага"
    assert data["product_price"] == 100
    assert data["factory_id"] == 1


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["product_name"] == "Тестовая бумага"
    assert data[0]["product_price"] == 100
    assert data[0]["factory_id"] == 1

def test_get_product_by_id():
    response = client.get("/products/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "Тестовая бумага"

def test_product_not_found():
    response = client.get("/products/3")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Product not found"


def test_create_contract():
    response = client.post(
        "/contracts/",
        json={"client_name": "Тестировщик", "address": "Тестовая 5", "date_arrangement" : "2020-10-19", "date_execution": "2021-10-19"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["client_name"] == "Тестировщик"


def test_add_order_to_product():
    response = client.post(
        "/products/1/orders/1/",
        json={
            "amount": 5, 
            "product_id": 1,
            "contract_id": 1
    }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["amount"] == 5
    assert data["product_id"] == 1
    assert data["contract_id"] == 1


def test_get_contract():
    response = client.get("/contracts/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["client_name"] == "Тестировщик"


def test_get_contract_by_id():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/contracts/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["client_name"] == "Тестировщик"

def test_contract_not_found():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/contracts/3")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contract not found"



def test_get_order():
    response = client.get("/orders/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["amount"] == 5

def test_get_order_by_id():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/orders/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["amount"] == 5


def test_order_not_found():
    """
    Проверка случая, если пользователь с таким id отсутствует в БД
    """
    response = client.get("/orders/3")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Order not found"