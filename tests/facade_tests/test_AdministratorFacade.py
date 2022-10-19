import pytest

from db.db_config import local_session
from db.db_repo import DbRepo
from db.facades.AnonymousFacade import AnonymousFacade
from db.tables.Administrators import Administrators
from db.tables.AirlineCompanies import AirlineCompanies
from db.tables.Customers import Customers
from db.tables.Users import Users
from errors import AirlineAlreadyExistException, CustomerAlreadyExistException, WrongInstanceException


repo = DbRepo(local_session)


@pytest.fixture(scope='session')
def dao():
    anon_facade = AnonymousFacade()
    return anon_facade.login('DeadPool3', '32345')


@pytest.fixture(autouse=True)
def reset():
    repo.reset_db()


def test_get_all_customers(dao):
    customers = repo.get_all(Customers)
    assert len(customers) == 2


def test_add_airline(dao):
    user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=2)
    airline = AirlineCompanies(name='Canada Airline', country_id=2, users_id=7)
    dao.add_airline(airline, user)
    assert airline in repo.get_all(AirlineCompanies)

def test_add_airline_raise_AirlineAlreadyExistException(dao):
    with pytest.raises(AirlineAlreadyExistException):
        user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=2)
        airline = AirlineCompanies(name='Delta', country_id=2, users_id=7)
        dao.add_airline(airline, user)

def test_add_customer(dao):
    user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=1)
    customer = Customers(first_name='Jane', last_name=' Paris', address='Toronto', phone_num='888-666',
                         credit_card_num='3477-222', users_id=7)
    dao.add_customer(customer, user)
    assert customer in repo.get_all(Customers)

def test_add_customer_raise_CustomerAlreadyExistException(dao):
    with pytest.raises(CustomerAlreadyExistException):
        user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=2)
        customer = Customers(first_name='Jane', last_name=' Paris', address='Toronto', phone_num='888-666',
                             credit_card_num='3477-222', users_id=1)
        dao.add_customer(customer, user)

def test_add_administrator(dao):
    user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=3)
    administrator = Administrators(first_name='Jane', last_name=' Paris', users_id=7)
    dao.add_administrator(administrator, user)
    assert administrator in repo.get_all(Administrators)

def test_add_administrator_raise_WrongInstanceException(dao):
    with pytest.raises(WrongInstanceException):
        user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=2)
        administrator = dao.repo.get_by_id(Administrators, 3)
        dao.add_administrator(administrator, user)

def test_remove_airline(dao):
    airline = dao.repo.get_by_id(AirlineCompanies, 2)
    dao.remove_airline(airline)
    airlines = dao.get_all_airline()
    assert airline not in airlines

def test_remove_airline_raise_WrongInstanceException(dao):
    with pytest.raises(WrongInstanceException):
        airline = dao.repo.get_by_id(AirlineCompanies, 3)
        dao.remove_airline(airline)

def test_remove_customer(dao):
    customer = dao.repo.get_by_id(Customers, 2)
    dao.remove_customer(customer)
    customers = dao.get_all_customers()
    assert customer not in customers

def test_remove_customer_raise_WrongInstanceException(dao):
    with pytest.raises(WrongInstanceException):
        customer = dao.repo.get_by_id(Customers, 3)
        dao.remove_customer(customer)

def test_remove_administrator(dao):
    administrator = dao.repo.get_by_id(Administrators, 2)
    dao.remove_administrator(administrator)
    administrators = dao.repo.get_all(Administrators)
    assert administrator not in administrators
