import enum

from sqlalchemy import Column, Integer, LargeBinary, String, Enum, Boolean

from core.database import Base
from util.models import TimestampCreateMixin, TimestampUpdateMixin

db_prefix = "dropi"


class DropType(enum.Enum):
    text = 0  # for plaintext
    source_code = 1  # for source (surprising right?)
    image = 2  # for images - jpeg compression
    document = 3  # pdf TODO word documents?
    file = 4  # downloadable file - TODO preview?
    folder = 5  # collection of downloadable files
    discussion = 6  # pseudonym based (group) chat


class DropStatus(enum.Enum):
    default = 0  # normal drop

    disabled = 1  # inaccessible for the public but the data is not yet deleted
    deleted = 2  # data has been deleted - either by the uploader or by an admin

    disabled_tos = 3  # inaccessible for the public due to violation of the term of service. investigation pending
    delete_tos = 4  # data has been deleted after investigation of tos breach is completed


# represents a drop in the database - who'd have thunk ._.
class Drop(TimestampCreateMixin, TimestampUpdateMixin, Base):
    __tablename__ = f"{db_prefix}_drop"

    id = Column(Integer, index=True, autoincrement=True)

    # drop metadata
    drop_status = Column(Enum(DropStatus))  # current status of the drop
    drop_type = Column(Enum(DropType))  # describes how the data should be interpreted
    drop_is_password_protected = Column(Boolean(), nullable=False)  # true if the data is encrypted with a password in addition to default encryption
    drop_views = Column(Integer)  # view counter of the drop

    # drop data
    # TODO documentation
    drop_data = Column(LargeBinary, nullable=False)  # encrypted binary data of the drop including title and description
    drop_token = Column(String, primary_key=True)

    # create info
    drop_created_by_user = Column(String)  # the user who created the drop
    drop_created_by_ip = Column(String, nullable=False)  # the ip-address the drop was created from

