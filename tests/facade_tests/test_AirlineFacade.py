from datetime import datetime

import pytest

from db.db_config import local_session
from db.db_repo import DbRepo
from db.facades.AnonymousFacade import AnonymousFacade
from db.tables.AirlineCompanies import AirlineCompanies
from db.tables.Flights import Flights
from errors import WrongInstanceException, OtherInstanceOfClassException, AirlineAlreadyExistException, \
    WrongParametersException, OtherRolePermissionsRequired

repo = DbRepo(local_session)


@pytest.fixture(scope='session')
def dao():
    anon_facade = AnonymousFacade()
    return anon_facade.login('DeadPool2', '22345')


@pytest.fixture(autouse=True)
def reset():
    repo.reset_db()


def test_update_airline(dao):
    airline = AirlineCompanies(id=2, name='USA airline', country_id=1, users_id=2)
    dao.update_airline(airline)
    assert airline.as_dict() in [item.as_dict() for item in dao.repo.get_all(AirlineCompanies)]

def test_update_airline_raise_WrongInstanceException(dao):
    with pytest.raises(WrongInstanceException):
        airline = dao.repo.get_by_id(AirlineCompanies, 3)
        dao.update_airline(airline)


def test_update_airline_raise_OtherInstanceOfClassException(dao):
    with pytest.raises(OtherInstanceOfClassException):
        airline = dao.repo.get_by_id(AirlineCompanies, 1)
        dao.update_airline(airline)

def test_update_airline_raise_AirlineAlreadyExistException(dao):
    with pytest.raises(AirlineAlreadyExistException):
        airline = AirlineCompanies(id=2, name='Delta', country_id=1, users_id=2)
        dao.update_airline(airline)

def test_add_flight(dao):
    flight = Flights(airline_company_id=1, origin_country_id=2, destination_country_id=1,
                     departure_time=datetime(2022, 2, 4, 11, 30, 2), landing_time=datetime(2022, 2, 4, 14, 45, 2),
                     remaining_tickets=89)
    dao.add_flight(flight)
    assert flight in repo.get_all(Flights)

def test_add_flight_raise_WrongParametersException(dao):
    with pytest.raises(WrongParametersException):
        flight = Flights(airline_company_id=1, origin_country_id=2, destination_country_id=2,
                     departure_time=datetime(2022, 2, 4, 11, 30, 2), landing_time=datetime(2022, 2, 4, 14, 45, 2),
                     remaining_tickets=89)
        dao.add_flight(flight)

def test_update_flight(dao):
    flight = Flights(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                     departure_time=datetime(2022, 2, 3, 11, 30, 2), landing_time=datetime(2022, 2, 4, 14, 45, 2),
                     remaining_tickets=89)
    dao.update_flight(flight)
    assert flight.as_dict() in [item.as_dict() for item in dao.repo.get_all(Flights)]


def test_remove_flight(dao):
    flight = dao.repo.get_by_id(Flights, 2)
    dao.remove_flight(flight)
    flights = dao.get_all_flights()
    assert flight not in flights

def test_remove_flight_raise_WrongInstanceException(dao):
    with pytest.raises(WrongInstanceException):
        flight = dao.repo.get_by_id(Flights, 3)
        dao.remove_flight(flight)

def test_get_my_flight(dao):
    assert dao.get_my_flights() != 0

