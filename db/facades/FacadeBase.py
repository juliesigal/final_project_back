from abc import ABC, abstractmethod
from sqlalchemy import extract

from db.LoginToken import LoginToken
from db.db_config import local_session
from db.db_repo import DbRepo
from db.tables.AirlineCompanies import AirlineCompanies
from db.tables.Countries import Countries
from db.tables.Flights import Flights
from db.tables.Tickets import Tickets
from db.tables.Users import Users
from errors import UserAlreadyExistException, PasswordTooShortException, WrongInstanceException
from logger import Logger

class FacadeBase(ABC):

    @abstractmethod
    def __init__(self):
        self.repo = DbRepo(local_session)
        self.logger = Logger.get_instance()

    # @abstractmethod
    # def __init__(self, repo, login_token=LoginToken(id_=None, name='Anonymous', role='Anonymous')):
    #     self.logger = Logger.get_instance()
    #     self.repo = repo
    #     self._login_token = login_token
    #
    # @property
    # def login_token(self):
    #     return self._login_token

    def get_all_flights(self):
        return self.repo.get_all(Flights)

    def get_all_tickets(self):
        return self.repo.get_all(Tickets)

    def get_all_airline(self):
        return self.repo.get_all(AirlineCompanies)

    def get_flight_by_id(self, flight_id):
        return self.repo.get_by_id(Flights, flight_id)

    def get_flight_by_parameters(self, origin_country_id, destination_country_id, depart, land):
        column_names = [Flights.origin_country_id, Flights.destination_country_id, Flights.departure_time,
                        Flights.landing_time]
        info = [origin_country_id, destination_country_id, depart, land]

        return self.repo.get_by_condition(Flights,
                                          lambda query: query.filter(
                                              column_names[0] == info[0],
                                              column_names[1] == info[1],
                                              column_names[2] == info[2],
                                              column_names[3] == info[3],
                                          ).all())

    def get_airline_by_id(self, airline_id):
        return self.repo.get_by_id(AirlineCompanies, airline_id)

    def get_airline_by_parameters(self, name, country_id, users_id):
        column_names = [AirlineCompanies.name, AirlineCompanies.country_id, AirlineCompanies.users_id]
        info = [name, country_id, users_id]

        return self.repo.get_by_condition(AirlineCompanies,
                                          lambda query: query.filter(
                                              column_names[0] == info[0],
                                              column_names[1] == info[1],
                                              column_names[2] == info[2],
                                          ).all())


    def get_all_countries(self):
        return self.repo.get_all(Countries)

    def get_country_by_id(self, country_id):
        return self.repo.get_by_id(Countries, country_id)

    def create_new_user(self, user):
        if not isinstance(user, Users):
            self.logger.logger.error(f"User: {user} must be user's instance")
            raise WrongInstanceException
        """check if username/email unique+password not too short"""
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == user.username)).all():
            self.logger.logger.error(f'User with this username: {user.username} already exist')
            raise UserAlreadyExistException
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.email == user.email)).all():
            self.logger.logger.error(f'User with this email: {user.email} already exist')
            raise UserAlreadyExistException
        if len(user.password) < 4:
            self.logger.logger.error('Password is too short!')
            raise PasswordTooShortException
        self.logger.logger.info(f"Creating new user: {user}")
        self.repo.add(user)
