import os
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.db.utils import get_db_type


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
