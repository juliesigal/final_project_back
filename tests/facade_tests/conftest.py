import pytest

from db.facades.CustomerFacade import CustomerFacade
from db.tables.Flights import Flights


# @pytest.fixture(scope='session', autouse=True)
# def customer_facade():
#     return CustomerFacade()
#
#
# @pytest.fixture(scope='function')
# def test_flight():
#     flights = Flights()
#     flights.add_flight()
