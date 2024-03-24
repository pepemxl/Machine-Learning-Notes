from datetime import datetime
import os
from sqlalchemy import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.schema import UniqueConstraint
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(package_path)
from pp_tools.db.schema_base import Base


class TblSnykProjects(Base):
    __tablename__ = 'tbl_snyk_projects'

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    name: Mapped[int] = mapped_column(
        String(45),
        nullable=False,
    )
    vulnerabilities = relationship('TblSnykVulnerabilities', back_populates='project')
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
        UniqueConstraint('name'),
    )


class TblSnykVulnerabilities(Base):
    __tablename__ = 'tbl_snyk_vulnerabilities'

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    name: Mapped[int] = mapped_column(
        String(45),
        nullable=False,
    )
    severity: Mapped[str] = mapped_column(
        String(45)
    )
    package_name: Mapped[str] = mapped_column(
        String(45)
    )
    package_version: Mapped[str] = mapped_column(
        String(45)
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_snyk_projects.id')
    )
    project = relationship('TblSnykProjects', back_populates='vulnerabilities')
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Date created',
        default=datetime.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Date Updated',
        default=datetime.now(), 
        onupdate=datetime.now()
    )

