from typing import List
from sqlalchemy import create_engine, Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base

# initialize SQLAlchemy
Base = declarative_base()
engine = create_engine("sqlite:///sqlite.db")


# define the table structure
class Channels(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    timeout = Column(Integer)
    active = Column(Boolean, default=True)
    messages: Mapped[List["Messages"]] = relationship()


class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))


# create the table
Base.metadata.create_all(engine)

# start a session
Session = sessionmaker(bind=engine)
session = Session()
