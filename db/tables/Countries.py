from sqlalchemy import Column, BigInteger, String

from db.db_config import Base


class Countries(Base):
    __tablename__ = 'country'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'\n<Country id={self.id} country_name={self.name}>'

    def __str__(self):
        return self.__repr__()

    def get_dict(self):
        return {"id": self.id, "name": self.name}
