from datetime import datetime, time

from sqlalchemy import Column, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

from db.db_config import Base


class Flights(Base):
    __tablename__ = 'flight'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id', ondelete='CASCADE'), unique=False)
    origin_country_id = Column(BigInteger(), ForeignKey('country.id', ondelete='CASCADE'), unique=False)
    destination_country_id = Column(BigInteger(), ForeignKey('country.id', ondelete='CASCADE'), unique=False)
    departure_time = Column(DateTime(), nullable=False)
    landing_time = Column(DateTime(), nullable=False)
    remaining_tickets = Column(Integer(), nullable=False)

    airline_id = relationship('AirlineCompanies', backref=backref('flight', uselist=True, passive_deletes=True))
    origin_countries_id = relationship('Countries', foreign_keys=[origin_country_id], uselist=True,
                                       passive_deletes=True)
    destination_countries_id = relationship('Countries', foreign_keys=[destination_country_id], uselist=True,
                                            passive_deletes=True)

    def as_dict(self):
        obj_dict = {}
        for c in self.__table__.columns:
            type_datetime = isinstance(getattr(self, c.name), datetime)
            type_time = isinstance(getattr(self, c.name), time)
            if type_datetime or type_time:
                obj_dict[c.name] = str(getattr(self, c.name))
            else:
                obj_dict[c.name] = getattr(self, c.name)
        return obj_dict

    #     def get_dict(self):
    #         return {"id": self.id, "name": self.name}

    def __repr__(self):
        return f'\n<Flight id={self.id}, airline_company_id={self.airline_company_id}, ' \
               f'origin_country_id={self.origin_country_id}, ' \
               f'destination_country_id={self.destination_country_id}, ' \
               f'departure_time={self.departure_time}, landing_time={self.landing_time}, ' \
               f'remaining_tickets={self.remaining_tickets}>'

    def __str__(self):
        return self.__repr__()
