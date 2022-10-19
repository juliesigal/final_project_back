from db.facades.FacadeBase import FacadeBase
from db.tables.Customers import Customers
from db.tables.Flights import Flights
from db.tables.Tickets import Tickets
from errors import NoMoreTicketsForFlightsException, CustomerAlreadyExistException, FlightNotFoundException, \
    OtherRolePermissionsRequired, WrongInstanceException, ObjectNotExistException, \
    OtherInstanceOfClassException, UniqueConstraintAlreadyExist
from logger import Logger


class CustomerFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.logger = Logger.get_instance()
        self.login_token = login_token

    def update_customer(self, customer):
        if self.login_token.role != 'Customer':
            self.logger.logger.error(
                f"Login token: {self.login_token},Customer's permissions required to update customers")
            raise OtherRolePermissionsRequired()
        if not isinstance(customer, Customers):
            self.logger.logger.error(f"Login token: {self.login_token}, Object must to be customer instance!")
            raise WrongInstanceException()
        current_customer = self.repo.get_by_condition(Customers, lambda query: query.filter(
            Customers.id == customer.id).all())
        if not current_customer:
            self.logger.logger.error(f"Login token: {self.login_token}, Customer with this id not exist")
            raise ObjectNotExistException
        if current_customer[0].id != self.login_token.id:
            self.logger.logger.error(
                f"Login token: {self.login_token}:Other customer {customer} tried to update the parameters")
            raise OtherInstanceOfClassException
        if current_customer[0].phone_num != customer.phone_num:
            if self.repo.get_by_condition(Customers,
                                          lambda query: query.filter(Customers.phone_num == customer.phone_num).all()):
                self.logger.logger.error(
                    f"Login token: {self.login_token}: Phone number {customer.phone_num} must be unique")
                raise CustomerAlreadyExistException
        if current_customer[0].credit_card_num != customer.credit_card_num:
            if self.repo.get_by_condition(Customers, lambda query: query.filter(
                    Customers.credit_card_num == customer.credit_card_num).all()):
                self.logger.logger.error(
                    f"Login token: {self.login_token}: Credit card number {customer.credit_card_num} must be unique")
                raise CustomerAlreadyExistException
        if current_customer[0].users_id != customer.users_id:
            if self.repo.get_by_condition(Customers, lambda query: query.filter(
                    Customers.users_id == customer.users_id).all()):
                self.logger.logger.error(f"Login token: {self.login_token}:User id {customer.users_id} must be unique")
                raise CustomerAlreadyExistException
        self.logger.logger.info(f'Login token: {self.login_token}: Updating customer {customer}')
        self.repo.update_by_id(Customers, Customers.id, customer.id, customer.as_dict())

    def add_ticket(self, ticket):
        if not isinstance(ticket, Tickets):
            self.logger.logger.error(f"Login token: {self.login_token}: Object must to be ticket instance!")
            raise WrongInstanceException()
        if self.login_token.role != 'Customer':
            self.logger.logger.error(f"Login token: {self.login_token}: Customer's permissions required to add ticket")
            raise OtherRolePermissionsRequired()
        """" check if flight exist """
        flight = self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == ticket.flight_id)).all()
        if not flight:
            self.logger.logger.error(
                f"Login token: {self.login_token}: try to add ticket with flight id that not exist")
            raise FlightNotFoundException()
        if flight[0].remaining_tickets < 1:
            self.logger.logger.error(f"Login token: {self.login_token}:"
                                     f" No more tickets left for flight id: {flight[0].id}, for customer id: {flight[0].customer_id}")
            raise NoMoreTicketsForFlightsException
        if self.repo.get_by_condition(Tickets, lambda query: query.filter(Tickets.flight_id == ticket.flight_id,
                                                                          Tickets.customer_id == ticket.customer_id).all()):
            self.logger.logger.error(f'Login token: {self.login_token}: This unique constraint '
                                     f'of customer id: {ticket.customer_id} and flight id: {ticket.flight_id} already exist')
            raise UniqueConstraintAlreadyExist
        self.logger.logger.info(f'Login token: {self.login_token}: Updating remaining tickets for flight: {flight[0].id}')
        flight[0].remaining_tickets -= 1
        self.logger.logger.info(f'Login token: {self.login_token}: Adding ticket {ticket}')
        self.repo.add(ticket)

    def remove_ticket(self, ticket):
        if not isinstance(ticket, Tickets):
            self.logger.logger.error(f"Login token: {self.login_token}: Object must to be ticket instance!")
            raise WrongInstanceException()
        if self.login_token.role != 'Customer':
            self.logger.logger.error(f"Login token: {self.login_token}:Customer's permissions required to add ticket")
            raise OtherRolePermissionsRequired()
        if not ticket.id:
            self.logger.logger.error(f"Login token: {self.login_token}: This ticket doesn't exist in the db")
            print(f"The ticket id doesn't exist in db")
        flight = self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == ticket.flight_id).all())
        self.logger.logger.info(f"Login token: {self.login_token}: updating remaining tickets.")
        flight[0].remaining_tickets += 1
        self.logger.logger.info(f"Login token: {self.login_token}: delete ticket {ticket}")
        self.repo.delete_by_id(Tickets, Tickets.id, ticket.id)

    def get_my_ticket(self):
        self.logger.logger.info(f'Login token: {self.login_token}: Getting my tickets')
        return self.repo.get_by_condition(Tickets,
                                          lambda query: query.filter(Tickets.customer_id == self.login_token.id)).all()
