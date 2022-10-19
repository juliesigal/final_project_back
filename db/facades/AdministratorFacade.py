from db.facades.FacadeBase import FacadeBase
from db.tables.Administrators import Administrators
from db.tables.AirlineCompanies import AirlineCompanies
from db.tables.Customers import Customers
from db.tables.Users import Users
from errors import AirlineAlreadyExistException, CustomerAlreadyExistException, \
    OtherRolePermissionsRequired, WrongInstanceException
from logger import Logger


class AdministratorFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token
        self.logger = Logger.get_instance()

    def get_all_customers(self):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(f"Administrator's permissions required to get all customers")
            raise OtherRolePermissionsRequired()
        return self.repo.get_all(Customers)

    def add_customer(self, customer, user):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(f"Administrator's permissions required to get all customers")
            raise OtherRolePermissionsRequired()
        if not isinstance(customer, Customers):
            self.logger.logger.error(f"The login_token: '{self.login_token.id}' tried to use the function 'add_customer"
                                     f" but the customer '{customer}' that was sent is not a Customer object")
            raise WrongInstanceException()
        if not isinstance(user, Users):
            self.logger.logger.error(f"The login_token '{self.login_token}' tried to use the function 'add_customer"
                                     f" but the user '{user}' that was sent is not a User object")
            raise WrongInstanceException()
        """check if id/phone num/credit card/user id unique. check if user id role 3"""
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_num == customer.phone_num).all()):
            self.logger.logger.error(f"Customer with this phone number: {customer.phone_num} already exist")
            raise CustomerAlreadyExistException()
        if self.repo.get_by_condition(Customers, lambda query: query.filter(
                Customers.credit_card_num == customer.credit_card_num).all()):
            self.logger.logger.error(f"Login token {self.login_token} tried to add Customer with exist"
                                     f" credit card number:{customer.credit_card_num} that already exist")
            raise CustomerAlreadyExistException()
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.users_id == customer.users_id).all()):
            self.logger.logger.error(f"Login token: {self.login_token},Customer with this user id: {customer.users_id} number already exist")
            raise CustomerAlreadyExistException()
        if self.create_new_user(user):
            if user.user_role_id != 1:
                self.logger.logger.error(f"User's role must be 1(customer) and not: {user.user_role_id}")
                print('User role must be 1(customer)')
        self.repo.add(customer)
        self.logger.logger.info(f"Login token: {self.login_token} creating new customer: {customer}")

    def add_airline(self, airline, user):  #check if airline user id/name unique, #check if this user has user role 2
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(f"Administrator's permissions required to get all customers")
            raise OtherRolePermissionsRequired()
        if not isinstance(airline, AirlineCompanies):
            self.logger.logger.error(f"The login_token '{self.login_token}' tried to use the function 'add_airline"
                                     f" but the user '{airline}' that was sent is not an Airline's object")
            raise WrongInstanceException()
        if not isinstance(user, Users):
            self.logger.logger.error(f"The login_token '{self.login_token}' tried to use the function 'add_airline"
                                     f" but the user '{user}' that was sent is not a User object")
            raise WrongInstanceException()
        if self.repo.get_by_condition(AirlineCompanies,
                                      lambda query: query.filter(AirlineCompanies.name == airline.name).all()):
            self.logger.logger.error(f"Airline with this name: {airline.name} already exist!")
            raise AirlineAlreadyExistException()
        if self.repo.get_by_condition(AirlineCompanies,
                                      lambda query: query.filter(AirlineCompanies.users_id == airline.users_id).all()):
            self.logger.logger.error(f"Airline with this user id: {airline.users_id} already exist!")
            raise AirlineAlreadyExistException()
        if self.create_new_user(user):
            if user.user_role_id != 2:
                self.logger.logger.error(f"User's role must be 2(airline) and not {user.user_role_id}")
                print('User role must be 2(airline)')
        self.repo.add(airline)
        self.logger.logger.info(f"Creating new airline {airline}")

    def add_administrator(self, administrator, user):
        """ check if id/user id unique #check if this user has user role 1 """
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(f"Administrator's permissions required to get all customers")
            raise OtherRolePermissionsRequired()
        if not isinstance(administrator, Administrators):
            self.logger.logger.error(f"Object {administrator} must be an administrator's instance")
            raise WrongInstanceException()
        if not isinstance(user, Users):
            self.logger.logger.error(f"Object {user} must be an user's instance")
            raise WrongInstanceException()
        if self.repo.get_by_condition(Administrators,
                                      lambda query: query.filter(
                                          Administrators.users_id == administrator.users_id).all()):
            self.logger.logger.error(f"Airline with this user id: {administrator.users_id} already exist")
            raise AirlineAlreadyExistException()
        if self.create_new_user(user):
            if user.user_role_id != 3:
                self.logger.logger.error(f"User role mast be 3(administrator) and not {user.user_role_id}!")
                print('User role must be 3(administrator)')
        self.logger.logger.info(f'Creating new administrator {administrator}')
        self.repo.add(administrator)

    def remove_airline(self, airline):
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(f"Administrator's permissions required to get all customers")
            raise OtherRolePermissionsRequired()
        if not isinstance(airline, AirlineCompanies):
            self.logger.logger.error(f"Object {airline} must be an airline's instance")
            raise WrongInstanceException()
        """remove airline and also remove user of this airline"""
        user_air = self.repo.get_by_condition(Users, lambda query: query.filter(Users.id == airline.users_id).all())
        self.logger.logger.info(f'Removing airline: {airline} and user of this airline: {user_air}')
        self.repo.delete_by_id(Users, Users.id, user_air[0].id)

    def remove_customer(self, customer):
        # remove user by customer.user_id
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(f"Administrator's permissions required to get all customers")
            raise OtherRolePermissionsRequired()
        if not isinstance(customer, Customers):
            self.logger.logger.error(f"Object {customer} must be a customer's instance")
            raise WrongInstanceException()
        user_cus = self.repo.get_by_condition(Users, lambda query: query.filter(Users.id == customer.users_id).all())
        self.logger.logger.info(f'Removing customer: {customer} and his user: {user_cus}')
        self.repo.delete_by_id(Users, Users.id, user_cus[0].id)

    def remove_administrator(self, administrator):
        # remove user by administrator.user_id
        if self.login_token.role != 'Administrator':
            self.logger.logger.error(f"Administrator's permissions required to get all customers")
            raise OtherRolePermissionsRequired()
        if not isinstance(administrator, Administrators):
            self.logger.logger.error(f"Object {administrator} must be an administrator's instance")
            raise WrongInstanceException()
        user_admin = self.repo.get_by_condition(Users,
                                                lambda query: query.filter(Users.id == administrator.users_id).all())
        self.logger.logger.info(f'Removing administrator: {administrator} and his user: {user_admin}')
        self.repo.delete_by_id(Users, Users.id, user_admin[0].id)
