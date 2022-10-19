from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

from db.db_config import Base


class Administrators(Base):
    __tablename__ = 'administrator'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    users_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    user_id = relationship('Users', backref=backref('administrator', uselist=False, passive_deletes=True))

    def get_dict(self):
        return {"id": self.id, "first_name": self.name, "last_name": self.last_name, "users_id": self.users_id}

    def __repr__(self):
        return f'\n<Administrator id={self.id}, first_name={self.first_name} ' \
               f'last_name={self.last_name} user_id={self.users_id}>'

    def __str__(self):
        return self.__repr__()
