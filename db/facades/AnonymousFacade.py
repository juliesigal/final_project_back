from db.LoginToken import LoginToken
from db.facades.AdministratorFacade import AdministratorFacade
from db.facades.AirlineFacade import AirlineFacade
from db.facades.CustomerFacade import CustomerFacade
from db.facades.FacadeBase import FacadeBase
from db.tables.Customers import Customers
from db.tables.Users import Users
from errors import UserNotExistException, CustomerAlreadyExistException, WrongInstanceException
from logger import Logger


class AnonymousFacade(FacadeBase):

    def __init__(self):
        super().__init__()
        self.logger = Logger.get_instance()

    def login(self, username, password):
        """check if username/password exist and same user id"""
        user = self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == username,
                                                                            Users.password == password).all())
        if not user:
            self.logger.logger.error(f"Username: {username} or password: {password} is wrong!!!")
            raise UserNotExistException
        if user[0].user_role_id == 3:
            login_token = LoginToken(id=user[0].administrator.id, name=user[0].administrator.first_name,
                                     role='Administrator')
            self.logger.logger.info(f'Administrator {login_token.id} just logged in')
            return AdministratorFacade(login_token)
        elif user[0].user_role_id == 2:
            login_token = LoginToken(id=user[0].airline_companies.id, name=user[0].airline_companies.name,
                                     role='Airline')
            self.logger.logger.info(f'Airline {login_token.id} just logged in')
            return AirlineFacade(login_token)
        elif user[0].user_role_id == 1:
            login_token = LoginToken(id=user[0].customer.id, name=user[0].customer.first_name,
                                     role='Customer')
            self.logger.logger.info(f'Customer {login_token.id} just logged in')
            return CustomerFacade(login_token)
        else:
            self.logger.logger.error(f"Wrong user role id: {user[0].user_role_id}")
            return

    def add_customer(self, customer, user):
        if not isinstance(customer, Customers):
            self.logger.logger.error(f' Object {customer} must be instance of class customers!')
            raise WrongInstanceException
        if not isinstance(user, Users):
            self.logger.logger.error(f' Object must be instance of class users!')
            raise WrongInstanceException
        """check if id/phone num/credit card/user id unique. check if user id role 3"""
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_num == customer.phone_num).all()):
            self.logger.logger.error(f'Phone number {customer.phone_num} must be unique!')
            raise CustomerAlreadyExistException
        if self.repo.get_by_condition(Customers, lambda query: query.filter(
                Customers.credit_card_num == customer.credit_card_num).all()):
            self.logger.logger.error(f'Credit card number {customer.credit_card_num} must be unique!')
            raise CustomerAlreadyExistException
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.users_id == customer.users_id).all()):
            self.logger.logger.error(f'User id {customer.users_id} must be unique!')
            raise CustomerAlreadyExistException
        if self.create_new_user(user):
            if user.user_role_id != 1:
                self.logger.logger.error(f'Customer role must be 1!!!')
                print('Customer role must be 1!')
        self.logger.logger.info(f'Adding customer{customer}')
        self.repo.add(customer)
