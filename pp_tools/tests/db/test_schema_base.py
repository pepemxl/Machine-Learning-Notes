import datetime
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.constants import TEST_DATA_OUTPUT_PATH
from pp_tools.common.logger import get_logger
from pp_tools.db.schema_base import Base


log = get_logger(__file__, "INFO")


class TestTblUsersModel(unittest.TestCase):
    # Set up the test database
    def setUp(self):
        flag_local = False
        if flag_local:
            engine = create_engine("sqlite:///:memory:", echo=True)  # Use an in-memory SQLite database for testing
        else:
            PATH_DB = os.path.join(TEST_DATA_OUTPUT_PATH, "pp_tools.db")
            engine = create_engine("sqlite:///{0}".format(PATH_DB), echo=True)
        Base.metadata.create_all(bind=engine)
        log.info("Database {0} created".format(Base.metadata.schema))
        Session = sessionmaker(bind=engine)
        self.session = Session()

    # Tear down the test database
    def tearDown(self):
        self.session.close()

    # Test the creation of a TblUsers record
    def test_create_tbl_users(self):
        # Create a TblUsers instance
        date_string = '2024-03-03 12:00:00'
        date_format = '%Y-%m-%d %H:%M:%S'
        parsed_datetime = datetime.datetime.strptime(date_string, date_format)

        user = TblUsers(
            email='test2@example.com',
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


if __name__ == '__main__':
    unittest.main()
