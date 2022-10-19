from sqlalchemy import Column, String, BigInteger

from db.db_config import Base


class UserRoles(Base):
    __tablename__ = 'user_role'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)

    def get_dict(self):
        return {"id": self.id, "role_name": self.role_name}

    def __repr__(self):
        return f'\n<User_role_id={self.id} role_name={self.role_name}>'

    def __str__(self):
        return self.__repr__()
