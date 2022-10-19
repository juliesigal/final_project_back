from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

from db.db_config import Base
from db.tables.UserRoles import UserRoles


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    user_role_id = Column(BigInteger(), ForeignKey('user_role.id', ondelete='CASCADE'), unique=False)

    users_role = relationship(UserRoles, backref=backref('users', uselist=True, passive_deletes=True))

    def get_dict(self):
        return {"id": self.id, "username": self.username, "password": self.password, "email": self.email, "user_role_id": self.user_role_id}

    def __repr__(self):
        return f'\n<User id={self.id} username={self.username} password={self.password}' \
               f' email={self.email}, user_role_id={self.user_role_id}>'

    def __str__(self):
        return self.__repr__()
