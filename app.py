from db.db_config import local_session
from db.db_repo import DbRepo
from db.facades.AnonymousFacade import AnonymousFacade
from db.tables import AirlineCompanies, Tickets, Flights, Countries, Users
from db.tables.Customers import Customers
from logger import Logger
from db.db_repo_pool import DbRepoPoolSingleton

from flask_cors import CORS
import uuid  # for public id
from datetime import datetime, timedelta
from functools import wraps
import jwt
# imports for PyJWT authentication
# flask imports
from flask import Flask, request, jsonify, make_response, Response, render_template
from werkzeug.security import generate_password_hash, check_password_hash

# creates Flask object
app = Flask(__name__)

repool = DbRepoPoolSingleton.get_instance()
repo = repool.get_connection()
logger = Logger.get_instance()

app.config['SECRET_KEY'] = 'your secret key'
CORS(app)
anon_facade = AnonymousFacade()

# decorator for verifying the JWT
'''def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')
            # return 401 if token is not passed
        if not token:
            logger.logger.error(f'Token is missing, error 401')
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            if data['role_name'] == 'Customer'
            current_customer = repo.update_by_column_value(Users, Users.public_id, data['public_id'], data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid !!'}), 401

        # passes the current logged in user into the endpoint so
        # you have access to them
        # (you also just pass the data of the token, or whatever
        #  you want)
        return f(current_user, *args, **kwargs)
    return decorated
'''

@app.route("/")
def home():
    return render_template(home.html)

@app.route('/signup', methods=['POST'])  # add customer
def signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    new_user = Users(username=username, password=password, email=email, user_role=3)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']
    phone_number = request.form['phone_number']
    credit_card_number = request.form['credit_card_number']
    new_customer = Customers(first_name=first_name, last_name=last_name, address=address, phone_number=phone_number, credit_card_number=credit_card_number )
    anon_facade.add_customer(customer=new_customer, user=new_user)
    repool.return_connection(repo)
    return make_response(jsonify({'task': 'signup', 'status': 'success'}), 200)


@app.route('/countries', methods=['GET'])
def get_all_countries():
    countries: list[Countries] = anon_facade.get_all_countries()  # getting from facade list of countries
    countries_dict: list[dict] = [country.get_dict() for country in countries]  # parsing the countries objects to dict
    return make_response(jsonify(countries_dict), 200)


@app.route('/countries/<int:id_>', methods=['GET'])
def get_country_by_id(id_):
    country_to_get = anon_facade.get_country_by_id(id_) # getting from facade country by id
    country_dict = country_to_get.get_dict()
    return make_response(jsonify(country_dict), 200)


@app.route('/flights', methods=['GET'])
def get_all_flights():
    flights: list[Flights] = anon_facade.get_all_flights()  # getting from facade list of flights
    flights_dict: list[dict] = [flight.as_dict() for flight in flights]  # parsing the flights objects to dict
    return make_response(jsonify(flights_dict), 200)

@app.route('/flights/<int:id_>', methods=['GET'])
def get_flight_by_id(id_):
    flight_to_get = anon_facade.get_flight_by_id(id_)
    flight_dict = flight_to_get.as_dict()
    return make_response(jsonify(flight_dict), 200)

@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    tickets: list[Tickets] = anon_facade.get_all_tickets()  # getting from facade list of tickets
    tickets_dict: list[dict] = [ticket.get_dict() for ticket in tickets]  # parsing the tickets objects to dict
    return make_response(jsonify(tickets_dict), 200)

@app.route('/airlines', methods=['GET'])
def get_all_airlines():
    airlines: list[AirlineCompanies] = anon_facade.get_all_airline()  # getting from facade list of airlines
    airlines_dict: list[dict] = [airline_companies.as_dict() for airline_companies in airlines]  # parsing the airlines objects to dict
    return make_response(jsonify(airlines_dict), 200)

@app.route('/airlines/<int:id_>', methods=['GET'])
def get_airline_by_id(id_):
    airline_to_get = anon_facade.get_airline_by_id(id_)
    airline_to_get_dict = airline_to_get.as_dict()
    return make_response(jsonify(airline_to_get_dict), 200)

if __name__ == '__main__':
    app.run(debug=True)