from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship

from core.database import Base
from util.models import HexByteString, TimestampUpdateMixin, TimestampCreateMixin

user_groups = Table(
    "core_user_groups",
    Base.metadata,
    Column("user_id", ForeignKey("core_users.user_id"), primary_key=True),
    Column("group_id", ForeignKey("core_groups.group_id"), primary_key=True),
)

user_permissions = Table(
    "core_user_permissions",
    Base.metadata,
    Column("user_id", ForeignKey("core_users.user_id"), primary_key=True),
    Column("permission_id", ForeignKey("core_permissions.permission_id"), primary_key=True),
)

group_permissions = Table(
    "core_group_permissions",
    Base.metadata,
    Column("group_id", ForeignKey("core_groups.group_id"), primary_key=True),
    Column("permission_id", ForeignKey("core_permissions.permission_id"), primary_key=True),
)


class User(Base):
    __tablename__ = "core_users"

    user_id = Column(Integer, primary_key=True, index=True)

    auth = relationship("Auth", uselist=False)  # use_list for one to one
    permissions = relationship("Permission", secondary=user_permissions, back_populates="users")
    groups = relationship("Group", secondary=user_groups, back_populates="users")

    username = Column(String(64), unique=True, index=True)
    display_name = Column(String(), nullable=True)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def has_permission(self, permission: str) -> bool:
        return permission.lower() in self.permissions


class Group(Base):
    __tablename__ = "core_groups"

    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(64), )
    group_description = Column(String(256))

    users = relationship("User", secondary=user_groups, back_populates="groups")
    permissions = relationship("Permission", secondary=group_permissions, back_populates="groups")


class Auth(TimestampCreateMixin, TimestampUpdateMixin, Base):
    __tablename__ = "core_auth"
    user_id = Column(ForeignKey("core_users.user_id"), primary_key=True)
    bcrypt_hash = Column(HexByteString())
    scramble = Column(String())


# DB representation of a Permission that can be granted to users or groups for access control
class Permission(Base):
    __tablename__ = "core_permissions"

    permission_id = Column(Integer, primary_key=True, index=True)

    app_name = Column(String)
    permission_name = Column(String, unique=True, index=True)

    users = relationship("User", secondary=user_permissions)
    groups = relationship("Group", secondary=group_permissions)

    def __eq__(self, other):
        if type(other) is str:
            return True if self.permission_name == other else False
        return super(self).__eq__(other)

    def __str__(self):
        return self.permission_name


# DB representation of a log message for Admin UI
class LogEvent(TimestampCreateMixin, Base):
    __tablename__ = "core_log"

    log_id = Column(Integer, primary_key=True)
    log_content = Column(String, )
    app_name = Column(String, )


class DebugEvent(TimestampCreateMixin, Base):
    __tablename__ = "core_debug"

    debug_id = Column(Integer, primary_key=True)
    log_content = Column(String, )
    app_name = Column(String, )

    trace = Column(String)
