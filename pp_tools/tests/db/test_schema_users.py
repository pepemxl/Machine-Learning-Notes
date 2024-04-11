from datetime import datetime
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.constants import TEST_DATA_OUTPUT_PATH
from pp_tools.common.logger import get_logger
from pp_tools.db.schema_base import Base
from pp_tools.db.schema_users import TblProjects
from pp_tools.db.schema_users import TblUsers


log = get_logger(
    logger_name=__name__,
    logger_caller=__file__,
    flag_stdout=True
)


class TestTblUsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flag_in_memory = True
        if cls.flag_in_memory:
            cls.engine = create_engine("sqlite:///:memory:", echo=False)  # Use an in-memory SQLite database for testing
        else:
            PATH_DB = os.path.join(TEST_DATA_OUTPUT_PATH, "pp_tools.db")
            cls.engine = create_engine("sqlite:///{0}".format(PATH_DB), echo=False)
        TblUsers.metadata.create_all(bind=cls.engine)
        if cls.flag_in_memory:
            log.info("Database in memory created".format(TblUsers.metadata.schema))
        else:
            log.info("Database {0} created".format(TblUsers.metadata.schema))
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()

    # Set up before each test
    def setUp(self):
        pass

    # Tear down after each test
    def tearDown(self):
        pass

    def test_tbl_users_creation(self):
        metadata = MetaData()
        if self.flag_in_memory:
            metadata.reflect(bind=self.engine)
        else:
            metadata.reflect(bind=self.engine, schema=str(Base.metadata.schema))
        flag_table_created = False
        if TblUsers.__tablename__ in metadata.tables:
            flag_table_created = True
        self.assertTrue(flag_table_created)

    # Test the creation of a TblUsers record
    def test_create_user(self):
        # Create a TblUsers row
        date_string = '2024-03-03 12:00:00'
        date_format = '%Y-%m-%d %H:%M:%S'
        parsed_datetime = datetime.strptime(date_string, date_format)
        user = TblUsers(
            email='test@example.com',
            country_code=1,
            phone_number=123456789,
            created_at=parsed_datetime
        )
        # Add the user to the session and commit
        self.session.add(user)
        self.session.commit()
        # Query the user from the database
        retrieved_user = self.session.query(TblUsers).filter_by(email='test@example.com').first()
        # Assert that the retrieved user is not None
        self.assertIsNotNone(retrieved_user)
        # Assert that the values match the expected values
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertEqual(retrieved_user.country_code, 1)
        self.assertEqual(retrieved_user.phone_number, 123456789)
        self.assertEqual(str(retrieved_user.created_at), '2024-03-03 12:00:00')

    def test_read_user(self):
        date_string = '2024-03-03 12:00:00'
        date_format = '%Y-%m-%d %H:%M:%S'
        parsed_datetime = datetime.strptime(date_string, date_format)
        user = TblUsers(
            email='test2@example.com',
            country_code=1,
            phone_number=123456789,
            created_at=parsed_datetime
        )
        self.session.add(user)
        self.session.commit()
        read_user = self.session.query(TblUsers).filter_by(email='test2@example.com').first()
        self.assertIsNotNone(read_user)

    def test_update_user(self):
        date_string = '2024-03-03 12:00:00'
        date_format = '%Y-%m-%d %H:%M:%S'
        parsed_datetime = datetime.strptime(date_string, date_format)
        user = TblUsers(
            email='test3@example.com',
            country_code=1,
            phone_number=123456789,
            created_at=parsed_datetime
        )
        self.session.add(user)
        self.session.commit()
        retrieved_user = self.session.query(TblUsers).filter_by(email='test3@example.com').first()
        retrieved_user.country_code = 2
        retrieved_user.phone_number = 987654321
        self.session.add(retrieved_user)
        self.session.commit()
        retrieved_user2 = self.session.query(TblUsers).filter_by(email='test3@example.com').first()
        self.assertIsNotNone(retrieved_user2)
        self.assertEqual(retrieved_user2.email, 'test3@example.com')
        self.assertEqual(retrieved_user2.country_code, 2)
        self.assertEqual(retrieved_user2.phone_number, 987654321)
        self.assertEqual(str(retrieved_user2.created_at), '2024-03-03 12:00:00')

    def test_delete_user(self):
        date_string = '2024-03-03 12:00:00'
        date_format = '%Y-%m-%d %H:%M:%S'
        parsed_datetime = datetime.strptime(date_string, date_format)
        user = TblUsers(
            email='test4@example.com',
            country_code=1,
            phone_number=123456789,
            created_at=parsed_datetime
        )
        self.session.add(user)
        self.session.commit()
        stmt = delete(TblUsers).where(TblUsers.email == 'test4@example.com')
        self.session.execute(stmt)
        retrieved_user = self.session.query(TblUsers).filter_by(email='test4@example.com').first()
        self.assertIsNone(retrieved_user)
    
    # def test_delete2_user(self):
    #     date_string = '2024-03-03 12:00:00'
    #     date_format = '%Y-%m-%d %H:%M:%S'
    #     parsed_datetime = datetime.strptime(date_string, date_format)
    #     user = TblUsers(
    #         email='test5@example.com',
    #         country_code=1,
    #         phone_number=123456789,
    #         created_at=parsed_datetime
    #     )
    #     self.session.add(user)
    #     self.session.commit()
    #     self.session.query(TblUsers).filter(TblUsers.email == 'test5@example.com').delete()
    #     retrieved_user = self.session.query(TblUsers).filter_by(email='test5@example.com').first()
    #     self.assertIsNone(retrieved_user)


if __name__ == '__main__':
    unittest.main()
