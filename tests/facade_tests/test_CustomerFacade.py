import pytest

from db.db_config import local_session
from db.db_repo import DbRepo
from db.facades.AnonymousFacade import AnonymousFacade
from db.tables.Customers import Customers
from db.tables.Tickets import Tickets
from errors import FlightNotFoundException, WrongInstanceException, \
    OtherInstanceOfClassException, CustomerAlreadyExistException, UniqueConstraintAlreadyExist

repo = DbRepo(local_session)


@pytest.fixture(scope='session')
def dao():
    anon_facade = AnonymousFacade()
    return anon_facade.login('DeadPool1', '12345')


@pytest.fixture(autouse=True)
def reset():
    repo.reset_db()


@pytest.mark.parametrize('ticket, expected', [(Tickets(flight_id=1, customer_id=1), True),
                                              (Tickets(flight_id=2, customer_id=2), True)])
def test_customer_facade_add_ticket(dao, ticket, expected):
    dao.add_ticket(ticket)
    assert expected


def test_flight_not_found(dao):
    with pytest.raises(FlightNotFoundException):
        ticket = Tickets(flight_id=3, customer_id=2)
        dao.add_ticket(ticket)

def test_unique_constraint_already_exist(dao):
    with pytest.raises(UniqueConstraintAlreadyExist):
        ticket = Tickets(flight_id=2, customer_id=1)
        dao.add_ticket(ticket)

# @pytest.mark.parametrize('ticket, expected', [('ticket', None),
#                                               (Tickets(flight_id=1, customer_id=2), True)])
def test_customer_facade_remove_ticket(dao):
    ticket = dao.get_my_ticket()
    dao.repo.delete_by_id(Tickets, Tickets.id, ticket[0].id)
    tickets = dao.get_all_tickets()
    assert ticket not in tickets

def test_remove_ticket_not_instance(dao):
    with pytest.raises(WrongInstanceException):
        ticket = dao.repo.get_by_id(Tickets, 4)
        dao.remove_ticket(ticket)


def test_update_customer(dao):
    customer = Customers(id=1, first_name='Dave', last_name='Green', address='New Jersey', phone_num='185-000',
                         credit_card_num='4580-333', users_id=1)
    dao.update_customer(customer)
    assert customer.as_dict() in [item.as_dict() for item in dao.repo.get_all(Customers)]

def test_update_customer_not_the_same_instance(dao):
    with pytest.raises(OtherInstanceOfClassException):
        customer = Customers(id=2, first_name='Dave', last_name='Green', address='New Jersey', phone_num='185-000',
                         credit_card_num='4580-333', users_id=1)
        dao.update_customer(customer)

def test_update_customer_alredy_exist(dao):
    with pytest.raises(CustomerAlreadyExistException):
        customer = Customers(id=1, first_name='Dave', last_name='Green', address='New Jersey', phone_num='185-000',
                         credit_card_num='3477-2020', users_id=1)
        dao.update_customer(customer)


def test_get_my_ticket(dao):
    assert dao.get_my_ticket() != None
