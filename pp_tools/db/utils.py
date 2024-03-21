from sqlalchemy import URL
from sqlalchemy.dialects import mssql, postgresql, sqlite, mysql
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import CreateTable
import sys
if __name__  == '__main__':
    import os
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


def get_ddl_for_table(tbl_obj: DeclarativeBase, dialect:Dialect) -> str:
    if dialect is None:
        return CreateTable(tbl_obj.__table__).compile(bind=None)
    else:
        return CreateTable(tbl_obj.__table__).compile(dialect=dialect)


def get_mysql_ddl_for_table(tbl_obj: DeclarativeBase):
    return get_ddl_for_table(tbl_obj, dialect=mssql.dialect())


def get_postgresql_ddl_for_table(tbl_obj: DeclarativeBase):
    return get_ddl_for_table(tbl_obj, dialect=postgresql.dialect())


def get_sqlite_ddl_for_table(tbl_obj: DeclarativeBase):
    return get_ddl_for_table(tbl_obj, dialect=sqlite.dialect())


def get_mysql_ddl_for_table(tbl_obj: DeclarativeBase):
    return get_ddl_for_table(tbl_obj, dialect=mysql.dialect())


def print_schema_definition(metadata_obj):
    for table in metadata_obj.tables.values():
        print("| Column | Type | Comment |")
        print("| --- | --- | --- |")
        for col in table.c:
            comment = col.comment if col.comment is not None else ""
            print("|{0}|{1}|{2}|".format(col.name, col.type, comment))
        print("")





