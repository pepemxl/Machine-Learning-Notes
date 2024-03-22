import os
from sqlalchemy import MetaData
from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import CreateTable
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.constants import TEST_DATA_OUTPUT_PATH
from pp_tools.common.environment_variables import get_env_var
from pp_tools.common.utils import is_unittest


def get_db_type() -> str:
    # Determinar el tipo de base de datos
    if is_unittest():
        return "sqlite"
    value = get_env_var("DB_TYPE", "sqlite")
    return value


db_type = get_db_type()
if db_type == 'sqlite':
    metadata_obj = MetaData()
else:
    metadata_obj = MetaData(schema="pp_tools")


class Base(DeclarativeBase):
    metadata = metadata_obj
    __table_args__ = {'schema': metadata.schema}

    def get_dict_repr(self):
        for key in self.__table__.columns.keys():
            value = self.__getattribute__(key)
            yield key, value

    def __repr__(self) -> str:
        fields = ", ".join(["{0}={1}".format(key, value) for key, value in self.get_dict_repr()])
        return "{0} {1}".format(self.__class__.__name__, fields)


def get_url_object(drivername: str = "mysql", DBAPI: str = "pymysql"):
    if drivername == "mysql":
        if DBAPI:
            drivername = drivername + "+" + DBAPI
        url_object = URL.create(
            drivername=drivername,
            username=get_env_var("MYSQL_USER"),
            password=get_env_var("MYSQL_PASSWORD"),
            host=get_env_var("MYSQL_HOST"),
            port=get_env_var("MYSQL_PORT"),
            database=get_env_var("MYSQL_DATABASE")
        )
    if drivername == "sqlite":
        if is_unittest():
            db_filename = ":memory:"
            url_object = URL.create(
                drivername=drivername,
                database=db_filename
            )
        else:
            DATABASE = get_env_var("SQLITE_DATABASE")
            db_filename = DATABASE + ".db"
            PATH_DB = os.path.join(TEST_DATA_OUTPUT_PATH, db_filename)
            url_object = URL.create(
                drivername=drivername,
                database=PATH_DB
            )
    return url_object