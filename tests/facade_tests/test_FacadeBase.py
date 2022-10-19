import pytest

from db.db_config import local_session
from db.db_repo import DbRepo
from db.facades.FacadeBase import FacadeBase
from db.tables.Countries import Countries


@pytest.fixture(scope='session')
def dao():
    return FacadeBase()


repo = DbRepo(local_session)


# def test_get_country_by_id(dao):
#     assert repo.get_by_id(Countries, 2) != None
#
#
# def test_get_all_countries(dao):
#     countries = repo.get_all(Countries)
#     assert len(countries) == 2
#
#
# def test_get_airline_by_parameters(dao):
#     airline = dao.get_airline_by_parameters(name='Delta', country_id=1, users_id=7)
#     assert airline != None
#
#
# def test_get_airline_by_id(dao):
#     airline = dao.get_airline_by_id(1)
#     assert airline != None
#
#
# def test_get_flight_by_parameters(dao):
#     flight = dao.get_flight_by_parameters(origin_country_id=2, destination_country_id=1,
#                                           depart='2022-01-26 11:40:53.594813', land='2022-01-26 11:40:53.594813')
#     assert flight != None
#
# def test_get_flight_by_id(dao):
#     flight = dao.get_flight_by_id(3)
#     assert flight != None
#
# def test_get_all_flights(dao):
#     flights = dao.get_all_flights()
#     assert len(flights) == 2
#
# def test_get_all_airline(dao):
#     airline = dao.get_all_airline()
#     assert len(airline) == 2
