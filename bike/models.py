from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Bike(Base):
    __tablename__ = "bike_bikes"
    bike_id = Column(Integer(), primary_key=True)
    frame_serial_number = Column(String(64), unique=True)
    name = Column(String(256))
    owner = Column(String(256))
    missing = Column(Boolean())
    note = Column(String())
    frame_color = Column(ForeignKey("util_colors.Color"))

    images = relationship("util_colors.Image")  # for bidirectional access use backref="bike"

