--get airline by username
drop function if exists sp_get_airline_by_username;
CREATE or replace function sp_get_airline_by_username(_username character varying(50))
returns Table(id bigint, name character varying(50))
language plpgsql AS
    $$
        BEGIN
            return QUERY
            select a.id, a.name from airline_companies a
                 join users u on a.users_id = u.id
             where u.username = _username;
         end;
     $$;

--get customer by username
drop function if exists get_customer_by_username;
CREATE or replace function get_customer_by_username(_username character varying(50)
returns Table(id bigint, firs_name character varying(70), last_name character varying(70))
language plpgsql AS
    $$
        BEGIN
            return QUERY
            select c.id, c.first_name, c.last_name from customer c
                 join users u on c.users_id = u.id
             where u.username = _username;
         end;
     $$;

--get user by username
drop function if exists sp_get_user_by_username;
CREATE or replace function sp_get_user_by_username(_username text)
returns TABLE(id bigint, username  character varying(50), password  character varying(50), email  character varying(50))
language plpgsql AS
    $$
        BEGIN
			return query
            select u.id, u.username, u.password, u.email from users u
            where u.username = _username;
        end;
    $$;

--get flights by parameters
drop function if exists sp_get_flights_by_parameters;
CREATE or replace function sp_get_flights_by_parameters(_origin_country_id bigint, _destination_country_id bigint,
_date timestamp)
returns Table(id bigint, remaining_tickets integer)
language plpgsql AS
    $$
        BEGIN
            return QUERY
            select f.id, f.remaining_tickets from flight f
            where f.origin_country_id  = _origin_country_id and
			f.destination_country_id = _destination_country_id and
			f.departure_time = _date;
         end;
     $$;

--get flights by airline id
drop function if exists sp_get_flights_by_airline_id;
CREATE or replace function sp_get_flights_by_airline_id(_airline_company_id bigint)
returns Table(id bigint, remaining_tickets integer)
language plpgsql AS
    $$
        BEGIN
            return QUERY
            select f.id, f.remaining_tickets from flight f
            where f.airline_company_id  = _airline_company_id;
         end;
     $$;

--get arrival flights
drop function if exists sp_get_arrival_flights;
CREATE or replace function sp_get_arrival_flights(_country_id bigint)
returns Table(id bigint, airline_company_id bigint, destination_country_id bigint, origin_country_id bigint,
			  departure_time timestamp without time zone, landing_time timestamp, remaining_tickets int)
language plpgsql AS
    $$
        BEGIN
            return QUERY
            select * from  flight where (now() AT TIME ZONE 'UTC' + interval '12 hours') > flight.landing_time and
			flight.destination_country_id = _country_id;
         end;
     $$;

--get departure flights
drop function if exists sp_get_departure_flights;
CREATE or replace function sp_get_arrival_flights(_country_id bigint)
returns Table(id bigint, airline_company_id bigint, destination_country_id bigint, origin_country_id bigint,
			  departure_time timestamp without time zone, landing_time timestamp, remaining_tickets int)
language plpgsql AS
    $$
        BEGIN
            return QUERY
            select * from  flight where (now() AT TIME ZONE 'UTC' + interval '12 hours') > flight.departure_time and
			flight.origin_country_id = _country_id;
         end;
     $$;

--get tickets by customer
drop function if exists sp_get_tickets_by_customer;

CREATE or replace function sp_get_tickets_by_customer(_customer_id bigint)
returns Table(id bigint, flight_id bigint, customer_id bigint)
language plpgsql AS
    $$
        BEGIN
            return QUERY
            select t.id, t.flight_id, t.customer_id from ticket t
			   join customer c on t.customer_id = c.id
            where t.customer_id  = _customer_id;
         end;
     $$;
