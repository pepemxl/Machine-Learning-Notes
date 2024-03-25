from datetime import datetime
from enum import Enum
import os
from sqlalchemy import (
    DateTime,
    Enum, 
    Integer,
    String,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.schema import UniqueConstraint
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.db.schema_base import Base


class PushNotificationTypes(Enum):
    MOBILE = 'mobile'
    SMS = 'sms'
    EMAIL = 'email'


class TblUsers(Base):
    __tablename__ = 'tbl_users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    email: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        comment='User Email'
    )
    country_code: Mapped[int] = mapped_column(
        nullable=False,
        comment='Country Code'
    )
    phone_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment='Phone Number'
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Date created',
        default=datetime.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Date Updated',
        default=datetime.now(), 
        onupdate=datetime.now()
    )

    __table_args__ = (
        UniqueConstraint('email'),
    )


class TblDevices(Base):
    __tablename__ = 'tbl_devices'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    device_token: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        comment='User Email'
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_users.id', ondelete='CASCADE'),
        nullable=False,
        comment='Foreing key User Id',
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Date created',
        default=datetime.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Date Updated',
        default=datetime.now(),
        onupdate=datetime.now()
    )
    last_loggin_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        comment='last logging at',
        default=datetime.now(),
        onupdate=datetime.now()
    )

    __table_args__ = (
        UniqueConstraint('device_token'),
    )
