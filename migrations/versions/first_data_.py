"""empty message

Revision ID: first_data
Revises: 177a73894c4c
Create Date: 2022-11-03 17:01:40.702662

"""
from alembic import op
from sqlalchemy import orm
from datetime import datetime

from src.models import Factory, Product, Contract, Order


# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = '6db530161dcf' # тут у каждого свое значение
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    global_factory = Factory(factory_name='Всемирная фабрика', factory_director='Юрий Жижин', factory_phone='123-456')
    local_factory = Factory(factory_name='Местная фабрика', factory_director='Алексей Фанов', factory_phone='654-321')


    session.add_all([global_factory, local_factory])
    session.flush()

    long_contract = Contract(client_name='КанцФерма', address='Ул. Мира 12а', date_arrangement=datetime(2022, 1, 25, 10, 10), date_execution=datetime(2022, 6, 25, 10, 10))
    short_contract = Contract(client_name='КанцПарк', address='Ул. Конева 6б', date_arrangement=datetime(2022, 3, 12, 12, 10), date_execution=datetime(2022, 9, 20, 20, 5))
    medium_contract = Contract(client_name='Канцелярофф', address='Ул. Питонова 13в', date_arrangement=datetime(2021, 1, 12, 12, 10), date_execution=datetime(2022, 1, 12, 12, 10))
    large_contract = Contract(client_name='Моя канцелярия', address='Ул. Шарпоава 1', date_arrangement=datetime(2020, 3, 12, 12, 10), date_execution=datetime(2025, 10, 22, 11, 10))

    session.add_all([long_contract, short_contract, medium_contract, large_contract])
    session.flush()

    calendar = Product(product_name='Календарь 2022', product_price=100, factory_id = global_factory.id)
    magazine = Product(product_name='Журнал', product_price=500, factory_id = global_factory.id)
    paper = Product(product_name='Бумага А4', product_price=300, factory_id = local_factory.id)
    notebook = Product(product_name='Тетрадь', product_price=20, factory_id = local_factory.id)

    session.add_all([calendar, magazine, paper, notebook])
    session.commit()

    easy = Order(amount=5, product_id=calendar.id, contract_id=short_contract.id)
    big = Order(amount=200, product_id=paper.id, contract_id=large_contract.id)
    decent = Order(amount=10, product_id=magazine.id, contract_id=long_contract.id)
    normal = Order(amount=20, product_id=notebook.id, contract_id=medium_contract.id)

    session.add_all([easy, big, decent, normal])
    session.commit()



def downgrade() -> None:
    pass
