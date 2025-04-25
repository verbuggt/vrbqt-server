import base64

from sqlalchemy import String, Column, Integer, TypeDecorator, LargeBinary, DateTime, func
from sqlalchemy.orm import declarative_mixin

from core.database import Base

# DO NOT CHANGE - DATA LOSS - changing the prefix will result in creation of new tables!
db_prefix: str = "util"


@declarative_mixin
class TimestampCreateMixin:
    created_at = Column(DateTime, default=func.now())


@declarative_mixin
class TimestampUpdateMixin:
    changed_at = Column(DateTime, onupdate=func.now())


class HexByteString(TypeDecorator):
    """Convert Python bytestring to string with hexadecimal digits and back for storage."""

    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("HexByteString columns support only bytes values.")
        return value.hex()

    def process_result_value(self, value, dialect):
        return bytes.fromhex(value) if value else None


class Base64String(TypeDecorator):
    """Convert Python bytestring to string with hexadecimal digits and back for storage."""

    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("Base64String columns support only bytes values.")
        return base64.encodebytes(value)

    def process_result_value(self, value, dialect):
        return base64.decodebytes(value) if value else None


class Color(Base):
    __tablename__ = f"{db_prefix}_colors"
    color_id = Column(Integer(), primary_key=True)
    color_name = Column(String(64))

    color_rgb = Column(String(12))
    color_hex = Column(String(12))
    color_hsl = Column(String(12))


class Image(Base):
    __tablename__ = f"{db_prefix}_images"
    image_id = Column(Integer, primary_key=True)
    image_name = Column(String(256))
    image_description = Column(String(2048))
    image_data = Column(LargeBinary)


class Contact(Base):
    __tablename__ = f"{db_prefix}_contacts"
    image_id = Column(Integer, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    email_address = Column(String(512))
    primary_phone = Column(String(32))
    secondary_phone = Column(String(32))


class Address(Base):
    __tablename__ = f"{db_prefix}_addresses"
    image_id = Column(Integer, primary_key=True)
    address_name = Column(String(512))
    company_name = Column(String(512))
    street_name = Column(String(512))
    house_number = Column(Integer)
