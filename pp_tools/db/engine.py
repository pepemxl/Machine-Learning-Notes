from sqlalchemy import create_engine
from sqlalchemy import MetaData
if __name__  == '__main__':
    import sys
    import os
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.db.schema_base import get_url_object
from pp_tools.db.schema_snyk import Base as schema_snyk_base
from pp_tools.db.schema_users import Base as schema_users_base


def check_schema_consistency(
        schema_audited = schema_users_base,
        flag_consistency_from_database=False
        ):
    """
        @brief This function checks that class exist in database

        Notes:
        This project make use of same database to enable diferent
        environments. Then database against schema will be 
        deactivated by default
        TODO:
            - add field type consistency
    """
    flag = True
    url_object = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_object)
    metadata = MetaData()
    metadata.reflect(bind=engine, schema=str(schema_audited.metadata.schema))
    if flag_consistency_from_database:
        for table_name, table in metadata.tables.items():
            if table_name in schema_users_base.metadata.tables:
                class_table = schema_users_base.metadata.tables[table_name]
                if str(table) != str(class_table):
                    print(f"Schema mismatch for table {table_name}")
                    flag = False
            else:
                print(f"Table {table_name} exists in the database but not in class definitions")
                flag = False
    for table_name in schema_users_base.metadata.tables:
        if table_name in metadata.tables:
            class_table = schema_users_base.metadata.tables.get(table_name)
            db_table = metadata.tables.get(table_name)
            class_table_columns = set([str(col) for col in class_table.columns])
            db_table_columns = set([str(col) for col in db_table.columns])
            diff = class_table_columns-db_table_columns
            if diff:
                print(f"Columns {diff} exist in class but not in database")
                flag = False
            diff = db_table_columns-class_table_columns
            if diff:
                print(f"Columns {diff} exist in database but not in class")
                flag = False
        else:
            print(f"Table {table_name} is in class definitions but not in the database")
    return flag


def create_schema(schema_base=schema_users_base):
    url_object = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_object)
    schema_base.metadata.create_all(engine)


def create_schema_users():
    create_schema(schema_base=schema_users_base)


def create_kg_owners():
    create_schema(schema_base=schema_users_base)


def get_project_ref_from_schema_snyk(session, project_name='project 01'):
    from datetime import datetime
    from pp_tools.db.schema_snyk import TblSnykProjects
    existing_project = session.query(TblSnykProjects).filter_by(name=project_name).first()
    if not existing_project:
        project_ref = TblSnykProjects(name=project_name, created_at=datetime.now())
    else:
        project_ref = existing_project
    return project_ref


def test_schema_snyk():
    from datetime import datetime
    from sqlalchemy.orm import sessionmaker
    from pp_tools.db.schema_snyk import TblSnykProjects
    from pp_tools.db.schema_snyk import TblSnykVulnerabilities
    url_object = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_object)
    Session = sessionmaker(bind=engine)
    session = Session()

    proyecto_01 = get_project_ref_from_schema_snyk(session=session, project_name='project 01')
    proyecto_02 = get_project_ref_from_schema_snyk(session=session, project_name='project 02')
    proyecto_03 = get_project_ref_from_schema_snyk(session=session, project_name='project 03')
    proyecto_04 = get_project_ref_from_schema_snyk(session=session, project_name='project 04')
    proyecto_05 = get_project_ref_from_schema_snyk(session=session, project_name='project 05')
    vulne_01 = TblSnykVulnerabilities(name='CVE-2022-1234', severity='High', package_name='Package 1', package_version='1.0.0', created_at=datetime.now(), project=proyecto_01)
    vulne_02 = TblSnykVulnerabilities(name='CVE-2022-5678', severity='Medium', package_name='Package 2', package_version='2.0.0', created_at=datetime.now(), project=proyecto_02)
    vulne_03 = TblSnykVulnerabilities(name='CVE-2022-9012', severity='Low', package_name='Package 3', package_version='3.0.0', created_at=datetime.now(), project=proyecto_01)
    vulne_04 = TblSnykVulnerabilities(name='CVE-2022-12', severity='Low', package_name='Package 4', package_version='3.0.0', created_at=datetime.now(), project=proyecto_04)
    vulne_05 = TblSnykVulnerabilities(name='CVE-2022-12', severity='Low', package_name='Package 4', package_version='3.0.0', created_at=datetime.now(), project=proyecto_05)
    records = []
    records.append(proyecto_01)
    records.append(proyecto_02)
    records.append(proyecto_03)
    records.append(proyecto_04)
    records.append(vulne_01)
    records.append(vulne_02)
    records.append(vulne_03)
    records.append(vulne_04)
    records.append(vulne_05)
    session.add_all(records)
    try:
        session.commit()
    except Exception as e:
        print("An error ocurred:",str(e))
        session.rollback()
    finally:
        # Close the session
        session.close()
    

if __name__ == '__main__':
    # create_schema_users()
    # create_schema(schema_base=schema_snyk_base)
    # test_schema_snyk()
    check_schema_consistency(schema_audited=schema_users_base)
    # check_schema_consistency(schema_audited=schema_snyk_base)
    # Crear una base de datos SQLite en memoria
    
    #Session = sessionmaker(bind=engine)
    #session = Session()

