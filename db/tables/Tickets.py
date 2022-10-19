from sqlalchemy import Column, ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.orm import relationship, backref

from db.db_config import Base


class Tickets(Base):
    # association_table = Table('flight_customer', Base.metadata,
    #                           Column('flight_id', ForeignKey('flight.id'), primary_key=True),
    #                           Column('customer_id', ForeignKey('customer.id'), primary_key=True)
    #                           )
    __tablename__ = 'ticket'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flight.id', ondelete='CASCADE'), nullable=False, unique=False)
    customer_id = Column(BigInteger(), ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='una_1'),)

    flights = relationship('Flights', backref=backref('ticket', uselist=True, passive_deletes=True))
    customers = relationship('Customers', backref=backref('ticket', uselist=True, passive_deletes=True))


    def get_dict(self):
        return {"id": self.id, "flight_id": self.flight_id, "customer_id": self.customer_id}

    def __repr__(self):
        return f'\n<Ticket id={self.id} flight_id={self.flight_id} customer_id={self.customer_id}>'

    def __str__(self):
        return self.__repr__()
