from db.db_config import local_session, create_all_entities
from db.db_repo import DbRepo
from db.facades.AnonymousFacade import AnonymousFacade

create_all_entities()
from db.tables.Customers import Customers

repo = DbRepo(local_session)

#repo.drop_all_tables()
#customer_fac = CustomerFacade()
#admin_fac = AdministratorFacade()
anonymous_fac = AnonymousFacade()
#air_fac = AirlineFacade()

repo.reset_db()
customer1 = anonymous_fac.login('DeadPool1', '12345')