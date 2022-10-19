from datetime import datetime

from db.tables.Administrators import Administrators
from db.tables.AirlineCompanies import AirlineCompanies
from db.tables.Countries import Countries
from db.tables.Customers import Customers
from db.tables.Flights import Flights
from db.tables.Tickets import Tickets
from db.tables.UserRoles import UserRoles
from db.tables.Users import Users
from logger import Logger


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = Logger.get_instance()

    def get_by_id(self, table_class, id_to_get):
        return self.local_session.query(table_class).get(id_to_get)

    def get_all(self, table_class):
        return self.local_session.query(table_class).all()

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def delete_by_id(self, table_class, id_column_name, id_to_remove):
        self.local_session.query(table_class).filter(id_column_name == id_to_remove).delete(synchronize_session=False)
        self.local_session.commit()

    # def delete_by_id(self, table_class, id_column_name, id_to_remove):
    #     item_to_remove = self.local_session.query(table_class).filter(id_column_name == id_to_remove)
    #     item_to_remove.delete(synchronise_session=False)
    #     self.local_session.commit()

    def update_by_id(self, table_class, id_column_name, id_to_update, data):
        existing_object = self.local_session.query(table_class).filter(id_column_name == id_to_update)
        existing_object.update(data)
        self.local_session.commit()

    def get_airlines_by_country(self, country_id):
        return self.local_session.query(AirlineCompanies).filter(AirlineCompanies.country_id == country_id).all()

    def get_flights_by_origin_country_id(self, origin_country_id):
        return self.local_session.query(Flights).filter(Flights.origin_country_id == origin_country_id).all()

    def get_flights_by_destination_country_id(self, destination_country_id):
        return self.local_session.query(Flights).filter(Flights.destination_country_id == destination_country_id).all()

    def get_flight_by_departure_date(self, departure_time):
        return self.local_session.query(Flights).filter(Flights.departure_time == departure_time).all()

    def get_flight_by_landing_date(self, landing_time):
        return self.local_session.query(Flights).filter(Flights.landing_time == landing_time).all()

    def get_flight_by_customer(self, customer_id):
        ticket = self.local_session.query(Tickets).filter(Tickets.customer_id == customer_id).all()
        return self.local_session.query(Flights).filter(Flights.id == ticket.flight_id)

    def get_by_condition(self, table_class, cond):
        query_result = self.local_session.query(table_class)
        result = cond(query_result)
        return result

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(data)
        self.local_session.commit()

    def get_by_column_value(self, table_class, column_name, value):
        return self.local_session.query(table_class).filter(column_name == value).all()

    def get_by_i_like(self, table_class, column_name, exp):
        return self.local_session.query(table_class).filter(column_name.ilike(exp)).all()

    def update(self, object_to_update):
        self.local_session.update(object_to_update)
        self.local_session.commit()

    def create_all_sp(self, file):
        try:
            with open(file, 'r') as sp_file:
                queries = sp_file.read().split('|||')
            for query in queries:
                self.local_session.execute(query)
            self.local_session.commit()
            self.logger.logger.debug(f'All procedures from {file} were created.')
        except FileNotFoundError:
            self.logger.logger.critical(f'File "{file}" was not found')

    def drop_all_tables(self):
        self.local_session.execute('drop TABLE users CASCADE')
        self.local_session.execute('drop TABLE administrator CASCADE')
        self.local_session.execute('drop TABLE airline_companies CASCADE')
        self.local_session.execute('drop TABLE country CASCADE')
        self.local_session.execute('drop TABLE customer CASCADE')
        self.local_session.execute('drop TABLE flight CASCADE')
        self.local_session.execute('drop TABLE ticket CASCADE')
        self.local_session.execute('drop TABLE user_role CASCADE')
        self.local_session.commit()

    def reset_auto_inc(self, table_class):
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')

    def reset_auto_inc_all(self):
        self.local_session.execute(f'TRUNCATE TABLE administrator RESTART IDENTITY CASCADE')
        self.local_session.execute(f'TRUNCATE TABLE airline_companies RESTART IDENTITY CASCADE')
        self.local_session.execute(f'TRUNCATE TABLE country RESTART IDENTITY CASCADE')
        self.local_session.execute(f'TRUNCATE TABLE customer RESTART IDENTITY CASCADE')
        self.local_session.execute(f'TRUNCATE TABLE flight RESTART IDENTITY CASCADE')
        self.local_session.execute(f'TRUNCATE TABLE ticket RESTART IDENTITY CASCADE')
        self.local_session.execute(f'TRUNCATE TABLE user_role RESTART IDENTITY CASCADE')
        self.local_session.execute(f'TRUNCATE TABLE users RESTART IDENTITY CASCADE')
        self.local_session.commit()

    def reset_db(self):
        self.reset_auto_inc_all()
        self.add(Countries(name='Israel'))
        self.add(Countries(name='USA'))
        self.add(UserRoles(role_name='Customer'))
        self.add(UserRoles(role_name='Airline_company'))
        self.add(UserRoles(role_name='Administrator'))
        self.add(Users(username='DeadPool1', password='12345', email='dead1@pool.com', user_role_id=1))
        self.add(Users(username='DeadPool2', password='22345', email='dead2@pool.com', user_role_id=2))
        self.add(Users(username='DeadPool3', password='32345', email='dead3@pool.com', user_role_id=3))
        self.add(Users(username='DeadPool4', password='42345', email='dead4@pool.com', user_role_id=1))
        self.add(Users(username='DeadPool5', password='52345', email='dead5@pool.com', user_role_id=2))
        self.add(Users(username='DeadPool6', password='62345', email='dead6@pool.com', user_role_id=3))
        self.add(AirlineCompanies(name='Delta', country_id=1, users_id=5))
        self.add(AirlineCompanies(name='USA airline', country_id=2, users_id=2))
        self.add(Customers(first_name='Dave', last_name='Green', address='New Jersey', phone_num='182-932',
                           credit_card_num='4580-0101', users_id=1))
        self.add(Customers(first_name='Jane', last_name='Paris', address='Toronto', phone_num='876-554',
                           credit_card_num='3477-2020', users_id=4))
        self.add(Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                         departure_time=datetime(2022, 2, 3, 12, 50, 1), landing_time=datetime(2022, 2, 3, 16, 50, 1), remaining_tickets=89))
        self.add(Flights(airline_company_id=2, origin_country_id=2, destination_country_id=1,
                         departure_time=datetime(2022, 2, 4, 11, 30, 2), landing_time=datetime(2022, 2, 4, 14, 45, 2), remaining_tickets=89))
        self.add(Tickets(flight_id=1, customer_id=2))
        self.add(Tickets(flight_id=2, customer_id=1))
        self.add(Administrators(first_name='Diana', last_name='Grey', users_id=3))
        self.add(Administrators(first_name='Bob', last_name='Dylan', users_id=6))
