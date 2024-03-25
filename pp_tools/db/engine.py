from sqlalchemy import create_engine
from sqlalchemy import MetaData
if __name__  == '__main__':
    import sys
    import os
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.logger import get_logger
from pp_tools.db.schema_base import get_url_object
from pp_tools.db.schema_snyk import Base as schema_snyk_base
from pp_tools.db.schema_users import Base as schema_users_base


log = get_logger(__file__, "INFO")


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
    log.info("check_schema_consistency")
    flag = True
    url_object = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_object)
    metadata = MetaData()
    metadata.reflect(bind=engine, schema=str(schema_audited.metadata.schema))
    if flag_consistency_from_database:
        for table_name, table in metadata.tables.items():
            if table_name in schema_audited.metadata.tables:
                class_table = schema_audited.metadata.tables[table_name]
                if str(table) != str(class_table):
                    log.error(f"Schema mismatch for table {table_name}")
                    flag = False
            else:
                log.warning(f"Table {table_name} exists in the database but not in class definitions")
                flag = False
    for table_name in schema_audited.metadata.tables:
        if table_name in metadata.tables:
            class_table = schema_audited.metadata.tables.get(table_name)
            db_table = metadata.tables.get(table_name)
            class_table_columns = set([str(col) for col in class_table.columns])
            db_table_columns = set([str(col) for col in db_table.columns])
            diff = class_table_columns-db_table_columns
            if diff:
                log.error(f"Columns {diff} exist in class but not in database")
                flag = False
            diff = db_table_columns-class_table_columns
            if diff:
                log.error(f"Columns {diff} exist in database but not in class")
                flag = False
        else:
            log.error(f"Table {table_name} is in class definitions but not in the database")
    return flag


def create_schema(schema_base=schema_users_base):
    log.info("Creating Schema")
    url_object = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_object)
    try:
        schema_base.metadata.create_all(engine)
    except Exception as e:
        log.exception("Error creating schema {0}".format(str(e)))


def create_schema_users():
    create_schema(schema_base=schema_users_base)


def create_kg_owners():
    create_schema(schema_base=schema_users_base)


def get_project_ref_from_schema_snyk(
        session, 
        project_name,
        snyk_org_uuid,
        snyk_project_uuid,
        snyk_username,
        snyk_password,
        snyk_token
    ):
    from datetime import datetime
    from pp_tools.db.schema_snyk import TblSnykProjects
    existing_project = session.query(TblSnykProjects).filter(
        TblSnykProjects.name==project_name,
        TblSnykProjects.project_uuid==snyk_project_uuid,
        TblSnykProjects.org_uuid==snyk_org_uuid
    ).first()
    if not existing_project:
        log.info("Creating record for {0}".format(project_name))
        project_ref = TblSnykProjects(
            name=project_name,
            project_uuid=snyk_project_uuid,
            org_uuid=snyk_org_uuid,
            created_at=datetime.now()
        )
        project_ref.set_credentials(
            snyk_username,
            snyk_password,
            snyk_token
        )
        session.add(project_ref)
    else:
        log.info("Getting references for {0}".format(project_name))
        project_ref = existing_project
    return project_ref


def test_schema_snyk():
    from datetime import datetime
    from sqlalchemy.orm import sessionmaker
    from pp_tools.common.environment_variables import get_env_var
    from pp_tools.db.schema_snyk import TblSnykVulnerabilities
    
    url_object = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_object)
    Session = sessionmaker(bind=engine)
    session = Session()
    project_name = get_env_var("SNYK_PROJECT_NAME")
    snyk_org_uuid = get_env_var("SNYK_ORG_UUID")
    snyk_project_uuid = get_env_var("SNYK_PROJECT_UUID")
    snyk_username = get_env_var("SNYK_USERNAME")
    snyk_password = get_env_var("SNYK_PASSWORD")
    snyk_token = get_env_var("SNYK_TOKEN")
    proyecto_ref = get_project_ref_from_schema_snyk(
        session=session, 
        project_name=project_name,
        snyk_org_uuid=snyk_org_uuid,
        snyk_project_uuid=snyk_project_uuid,
        snyk_username=snyk_username,
        snyk_password=snyk_password,
        snyk_token=snyk_token
        )
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
    test_schema_snyk()
    # check_schema_consistency(schema_audited=schema_users_base)
    # check_schema_consistency(schema_audited=schema_snyk_base)
    # Crear una base de datos SQLite en memoria
    
    #Session = sessionmaker(bind=engine)
    #session = Session()

