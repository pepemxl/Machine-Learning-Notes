from datetime import datetime
import os
from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    LargeBinary,
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
from pp_tools.common.environment_variables import get_env_var
from pp_tools.common.utils import decrypt
from pp_tools.common.utils import encrypt
from pp_tools.db.schema_base import Base


APP_KEY_VALUE = get_env_var("APP_KEY")
APP_KEY = APP_KEY_VALUE.encode('utf-32')


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
        String(64),
        comment="Project name registered in snyk",
        nullable=False,
    )
    project_uuid: Mapped[str] = mapped_column(
        String(64),
        comment="uuid of project for snyk",
        default=""
    )
    org_uuid: Mapped[str] = mapped_column(
        String(64),
        comment="uuid of org for snyk",
        default=""
    )
    encrypted_username: Mapped[bytes] = mapped_column(
        LargeBinary,
        comment="Encrypted Username",
        default=""
    )
    encrypted_password: Mapped[bytes] = mapped_column(
        LargeBinary,
        comment="Encrypted Password",
        default=""
    )
    encrypted_token: Mapped[bytes] = mapped_column(
        LargeBinary,
        comment="Encrypted Token",
        default=""
    )
    snyk_created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Project Snyk Date of Creation',
        default=datetime.now()
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
        UniqueConstraint('name'),
    )

    def set_credentials(self, username, password, token):
        self.encrypted_username = encrypt(username, APP_KEY)
        self.encrypted_password = encrypt(password, APP_KEY)
        self.encrypted_token = encrypt(token, APP_KEY)

    def get_credentials(self):
        return (
            decrypt(self.encrypted_username, APP_KEY),
            decrypt(self.encrypted_password, APP_KEY),
            decrypt(self.encrypted_token, APP_KEY)
        )


class TblSnykVulnerabilitiesReports(Base):
    __tablename__ = 'tbl_snyk_vulnerabilities_reports'

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_snyk_projects.id')
    )
    last_test_date: Mapped[DateTime] = mapped_column(
        DateTime,
        comment='Last snyk test date',
        default=datetime.now()
    )
    origin: Mapped[str] = mapped_column(
        String(64),
        comment="Origin of report, example: cli",
        default="cli"
    )
    type: Mapped[str] = mapped_column(
        String(64),
        comment="Type of report, example pip",
    )
    total_dependencies: Mapped[int] = mapped_column(
        Integer,
        comment="Number of dependencies detected by snyk",
        default=0
    )
    number_issues_low_severity: Mapped[int] = mapped_column(
        Integer,
        comment="Number of issues with low severity",
        default=0
    )
    number_issues_medium_severity: Mapped[int] = mapped_column(
        Integer,
        comment="Number of issues with medium severity",
        default=0
    )
    number_issues_high_severity: Mapped[int] = mapped_column(
        Integer,
        comment="Numer of issues with high severity",
        default=0
    )
    number_issues_critical_severity: Mapped[int] = mapped_column(
        Integer,
        comment="Number of issues with critical severity",
        default=0
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


class TblSnykVulnerabilities(Base):
    __tablename__ = 'tbl_snyk_vulnerabilities'

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_snyk_projects.id'),
        nullable=False,
        comment="Foreign key tbl_snyk_projects.id"
    )
    report_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_snyk_vulnerabilities_reports.id'),
        nullable=False,
        comment="Foreign key tbl_snyk_vulnerabilities_reports.id"
    )
    library_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Library name"
    )
    library_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Library version"
    )
    library_version_remediation: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Library version recommended for remediation"
    )
    is_transitive: Mapped[bool] = mapped_column(
        Boolean,
        comment="Flag library is transive",
        default=False
    )
    severity: Mapped[str] = mapped_column(
        String(64),
        comment="Severity"
    )
    vulns: Mapped[str] = mapped_column(
        String(1024),
        comment="Concat of vulns comma separated"
    )
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


class TblSnykIssues(Base):
    __tablename__ = 'tbl_snyk_issues'

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    library_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Library name"
    )
    snyk_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Snyk issue id"
    )
    issue_type: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Snyk issue type"
    )
    title: Mapped[str] = mapped_column(
        String(128),
        comment="Snyk issue title"
    )
    severity: Mapped[str] = mapped_column(
        String(64),
        comment="Severity"
    )
    url: Mapped[str] = mapped_column(
        String(128),
        comment="Severity"
    )
    priotity_score: Mapped[int] = mapped_column(
        Integer,
        comment="Issue priority score"
    )
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