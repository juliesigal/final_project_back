import pytest

from db.db_config import local_session
from db.db_repo import DbRepo
from db.facades.AdministratorFacade import AdministratorFacade
from db.facades.AirlineFacade import AirlineFacade
from db.facades.AnonymousFacade import AnonymousFacade
from db.facades.CustomerFacade import CustomerFacade
from db.tables.Countries import Countries
from db.tables.Customers import Customers
from db.tables.Users import Users
from errors import UserNotExistException, CustomerAlreadyExistException, WrongInstanceException


@pytest.fixture(scope='session')
def dao():
    return AnonymousFacade()

@pytest.fixture(autouse=True)
def reset():
    repo.reset_db()


repo = DbRepo(local_session)


@pytest.mark.parametrize('username, password, expected', [('DeadPool1', '12345', CustomerFacade),
                                                          ('DeadPool2', '22345', AirlineFacade),
                                                          ('DeadPool3', '32345', AdministratorFacade)])
def test_annonymous_facade_login(dao, username, password, expected):
    actual = dao.login(username, password)
    assert isinstance(actual, expected)


def test_annonymous_facade_login_raise_Usernotexistsesception(dao):
    with pytest.raises(UserNotExistException):
        dao.login('dfgdgf', 'dfgdfg')


def test_add_customer(dao):
    user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=2)
    customer = Customers(first_name='Jan', last_name=' Pier', address='Paris', phone_num='324-567',
                         credit_card_num='5326-1013',
                         users_id=7)
    dao.add_customer(customer, user)
    assert repo.get_by_id(Customers, 3) != None


def test_annonymous_facade_add_customer_raise_CustomerAlreadyExistException(dao):
    with pytest.raises(CustomerAlreadyExistException):
        user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=2)
        customer = customer = Customers(first_name='Jan', last_name=' Pier', address='Paris', phone_num='876-554',
                         credit_card_num='5326-1013',
                         users_id=7)
        dao.add_customer(customer, user)

def test_annonymous_facade_add_customer_raise_WrongInstanceException(dao):
    with pytest.raises(WrongInstanceException):
        user = Users(username='DeadPool7', password='72345', email='dead7@pool.com', user_role_id=2)
        customer = dao.repo.get_by_id(Customers, 5)
        dao.add_customer(customer, user)


""" FacadeBase tests: """

def test_get_country_by_id(dao):
    assert repo.get_by_id(Countries, 2) != None


def test_get_all_countries(dao):
    countries = repo.get_all(Countries)
    assert len(countries) == 2


def test_get_airline_by_parameters(dao):
    airline = dao.get_airline_by_parameters(name='Delta', country_id=1, users_id=1)
    assert airline != None


def test_get_airline_by_id(dao):
    airline = dao.get_airline_by_id(2)
    assert airline != None


def test_get_flight_by_parameters(dao):
    flight = dao.get_flight_by_parameters(origin_country_id=2, destination_country_id=1,
                                          depart='2022-01-26 11:40:53.594813', land='2022-01-26 11:40:53.594813')
    assert flight != None

def test_get_flight_by_id(dao):
    flight = dao.get_flight_by_id(1)
    assert flight != None

def test_get_all_flights(dao):
    flights = dao.get_all_flights()
    assert len(flights) == 2

def test_get_all_airline(dao):
    airline = dao.get_all_airline()
    assert len(airline) == 2