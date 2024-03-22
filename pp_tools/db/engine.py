from sqlalchemy import create_engine
if __name__  == '__main__':
    import sys
    import os
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.db.schema_base import Base
from pp_tools.db.schema_base import get_url_object
from pp_tools.db.schema_users import TblUsers


def create_table_users():
    url_object = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_object)
    TblUsers.metadata.create_all(engine)
    print(url_object)


if __name__ == '__main__':
    create_table_users()
    # Crear una base de datos SQLite en memoria
    
    #Session = sessionmaker(bind=engine)
    #session = Session()
