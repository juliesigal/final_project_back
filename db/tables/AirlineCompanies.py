from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

from db.db_config import Base
from db.tables.Countries import Countries
from db.tables.Users import Users


class AirlineCompanies(Base):
    __tablename__ = 'airline_companies'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True, nullable=False)
    country_id = Column(BigInteger(), ForeignKey('country.id', ondelete='CASCADE'), unique=False)
    users_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    countries = relationship('Countries', backref=backref('airline_companies', uselist=True, passive_deletes=True))
    users = relationship('Users', backref=backref('airline_companies', uselist=False, passive_deletes=True))

    def as_dict(self):
        obj_dict = {}
        for c in self.__table__.columns:
            obj_dict[c.name] = getattr(self, c.name)
        return obj_dict

    def __repr__(self):
        return f'\n<AirlineCompany_id={self.id}, name={self.name} country_id={self.country_id},' \
               f' users_id={self.users_id}>'

    def __str__(self):
        return self.__repr__()
