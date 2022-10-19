from db.facades.FacadeBase import FacadeBase
from db.tables.AirlineCompanies import AirlineCompanies
from db.tables.Flights import Flights
from errors import AirlineAlreadyExistException, WrongInstanceException, \
    ObjectNotExistException, OtherInstanceOfClassException, WrongParametersException, OtherRolePermissionsRequired
from logger import Logger


class AirlineFacade(FacadeBase):

    def __init__(self, login_token):
        super().__init__()
        self.login_token = login_token
        self.logger = Logger.get_instance()

    def update_airline(self, airline):
        # check if id/name/user id is unique
        if self.login_token.role != 'Airline':
            self.logger.logger.error(
                f"Login token: {self.login_token}: Airline's permissions required to update an airline")
            raise OtherRolePermissionsRequired()
        if not isinstance(airline, AirlineCompanies):
            self.logger.logger.error(f"Login token: {self.login_token}:Airline must be an airline's instance")
            raise WrongInstanceException()
        current_airline = self.repo.get_by_condition(AirlineCompanies, lambda query: query.filter(
            AirlineCompanies.id == airline.id).all())

        if not current_airline:
            self.logger.logger.error(f"Login token: {self.login_token}:Airline with this id: {airline.id} not exist")
            raise ObjectNotExistException
        if current_airline[0].id != self.login_token.id:
            self.logger.logger.error(
                f"Login token: {self.login_token}:Other airline({airline.id})tried to update the parameters")
            raise OtherInstanceOfClassException
        if current_airline[0].name != airline.name:
            if self.repo.get_by_condition(AirlineCompanies,
                                          lambda query: query.filter(AirlineCompanies.name == airline.name).all()):
                self.logger.logger.error(f"Login token: {self.login_token}:This name({airline.name}) is not unique!")
                raise AirlineAlreadyExistException
        if current_airline[0].users_id != airline.users_id:
            if self.repo.get_by_condition(AirlineCompanies, lambda query: query.filter(
                    AirlineCompanies.users_id == airline.users_id).all()):
                self.logger.logger.error(
                    f"Login token: {self.login_token}:This user id({airline.users_id}) is not unique!")
                raise AirlineAlreadyExistException
        self.logger.logger.info(f'Login token: {self.login_token}:Updating airline{airline}')
        self.repo.update_by_id(AirlineCompanies, AirlineCompanies.id, airline.id, airline.as_dict())

    def update_flight(self, flight):  # check that origin != destination & check departure before landing
        if self.login_token.role != 'Airline':
            self.logger.logger.error(f"Login token: {self.login_token}: Must be an airline instance to update a flight")
            raise OtherRolePermissionsRequired
        if not isinstance(flight, Flights):
            self.logger.logger.error(f"Login token: {self.login_token}: Flight must be a flight's instance")
            raise WrongInstanceException()
        current_flight = self.repo.get_by_condition(Flights, lambda query: query.filter(
            Flights.id == flight.id).all())
        if not current_flight:
            self.logger.logger.error(f"Login token: {self.login_token}: Flight id ({flight.id}) to update is not found")
            raise ObjectNotExistException
        if current_flight[0].airline_company_id != self.login_token.id:
            self.logger.logger.error(
                f"Login token: {self.login_token}: Other airline{flight.airline_company_id} tried to update the parameters")
        if flight.origin_country_id == flight.destination_country_id:
            self.logger.logger.error(
                f"Login token: {self.login_token}: Origin country can't be the same to destination")
            raise WrongParametersException
        if flight.departure_time >= flight.landing_time:
            self.logger.logger.error(
                f"Login token: {self.login_token}: Departure time must be smaller than landing time")
            raise WrongParametersException
        self.logger.logger.info(f'Login token: {self.login_token}: Updating flight{flight}')
        self.repo.update_by_id(Flights, Flights.id, flight.id, flight.as_dict())

    def add_flight(self, flight):
        if self.login_token.role != 'Airline':
            self.logger.logger.error(f"Login token: {self.login_token}: Must be an airline instance to update a flight")
            raise OtherRolePermissionsRequired
        if not isinstance(flight, Flights):
            self.logger.logger.error(f"Login token: {self.login_token}: Flight must be a flight's instance")
            raise WrongInstanceException()
        if flight.origin_country_id == flight.destination_country_id:
            self.logger.logger.error(f"Login token: {self.login_token}:Origin country can't be the same to destination")
            raise WrongParametersException
        if flight.departure_time >= flight.landing_time:
            self.logger.logger.error(
                f"Login token: {self.login_token}: Departure time must be smaller than landing time")
            raise WrongParametersException
        self.logger.logger.info(f'Login token: {self.login_token}: Adding flight{flight}')
        self.repo.add(flight)

    def remove_flight(self, flight):
        if self.login_token.role != 'Airline':
            self.logger.logger.error(f"Login token: {self.login_token}:Must be an airline instance to update a flight")
            raise OtherRolePermissionsRequired
        if not isinstance(flight, Flights):
            self.logger.logger.error(f"Login token: {self.login_token}:Flight must be a flight's instance")
            raise WrongInstanceException()
        current_flight = self.repo.get_by_condition(Flights, lambda query: query.filter(
            Flights.id == flight.id).all())
        if not current_flight:
            self.logger.logger.error(f"Login token: {self.login_token}: Flight's id {flight.id} to remove is not found")
            raise ObjectNotExistException
        if current_flight[0].airline_company_id != self.login_token.id:
            self.logger.logger.error(
                f"Login token: {self.login_token}: Other airline {flight.id} tried to remove the flight")
        self.logger.logger.info(f'Login token: {self.login_token}: Removing my flights{flight}')
        self.repo.delete_by_id(Flights, Flights.id, flight.id)

    def get_my_flights(self):
        self.logger.logger.info(f'Login token: {self.login_token}: Getting my flights')
        return self.repo.get_by_condition(Flights, lambda query: query.filter(
            Flights.airline_company_id == self.login_token.id)).all()
