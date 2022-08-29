from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


import faker

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

# Таблица cars, где будут хранится авто
class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    brand = Column(String(60), nullable=False)
    color = Column(String(60), nullable=False)
    record_id = Column(Integer, ForeignKey(Record.id, ondelete="CASCADE"))

###------этот кусок кода использовался для заполнения базы --------
### стандартные 3 строки из примера
##engine = create_engine("sqlite:///mydatabase.db")
##Session = sessionmaker(bind=engine)
##session = Session()

##fake = faker.Faker("ru-Ru")
##
### заполняем данными базы
##for _ in range(4):
##    rec = Record(name=fake.name(),
##                 description=fake.job(),
##                 email=fake.email(),
##                 phone=fake.country_calling_code(),
##                 address=fake.address(),
##                 birthday=str(fake.date_of_birth()),
##                 created=str((datetime.now()).date()),
##                 done=True
##                 )
##    session.add(rec)
##session.commit()

##car = Car(brand="BMW", color="black", record_id=1)
##session.add(car)
##car = Car(brand="Volvo", color="white", record_id=2)
##session.add(car)
##car = Car(brand="VW", color="gray", record_id=3)
##session.add(car)
##car = Car(brand="Opel", color="blue", record_id=4)
##session.add(car)
##session.commit()

##for _ in range(4):
##    note = Note(note=fake.company())
##    session.add(note)          
##session.commit()

### пример полной выборки
##data_from_db = session.query(Record).all()
##for item in data_from_db:
##    print(f"{item.id}  {item.name}  {item.description}  {item.email}  \
##{item.phone}  {item.address}  {item.birthday}  \
##{item.created}")
##    print("")
##
### пример выборки по условию
##data1 = session.query(Record).filter(Record.id == 2).first()
##print(data1.name)
##
### пример удаления строки из базы
##session.query(Record).filter(Record.id == 4).delete()
##session.commit()
##-----------конец заполнения базы-------------------------
    
async def sql_context(app):
    url_db = f"sqlite:///{app['config']}/src/mydatabase.db"
    engine = create_engine(url_db)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    app['db_session'] = session
    yield
    app['db_session'].close()
