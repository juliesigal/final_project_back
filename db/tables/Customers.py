from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

from db.db_config import Base


class Customers(Base):
    __tablename__ = 'customer'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(String(70), nullable=False)
    last_name = Column(String(70), nullable=False)
    address = Column(String(70), nullable=False)
    phone_num = Column(String(50), unique=True, nullable=False)
    credit_card_num = Column(String(50), unique=True, nullable=False)
    users_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    users = relationship('Users', backref=backref('customer', uselist=False, passive_deletes=True))

    def as_dict(self):
        obj_dict = {}
        for c in self.__table__.columns:
            obj_dict[c.name] = getattr(self, c.name)

        return obj_dict



    def __repr__(self):
        return f'\n<Customer_id={self.id}, first_name={self.first_name}, last_name={self.last_name},' \
               f' address={self.address}, phone_num={self.phone_num},' \
               f' credit_card_num={self.credit_card_num}, users_id={self.users_id}>'

    def __str__(self):
        return self.__repr__()
