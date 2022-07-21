from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()

# Таблица records, где будут храниться записи о персонах
class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(String(150), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(150), nullable=False)
    birthday = Column(String(150), nullable=False)
    created = Column(String(30), nullable=False)
    done = Column(Boolean, default=True)

# Таблица notes, где будут храниться заметки
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    note = Column(String(100), nullable=False)
    created = Column(DateTime, default=datetime.now())
