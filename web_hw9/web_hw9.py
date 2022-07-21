from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from models import Record, Note

import faker
from datetime import datetime

# стандартные 3 строки из примера
engine = create_engine("sqlite:///myrecords.db")
Session = sessionmaker(bind=engine)
session = Session()

fake = faker.Faker("ru-Ru")

# заполняем данными базы
for _ in range(4):
    rec = Record(name=fake.name(),
                 description=fake.job(),
                 email=fake.email(),
                 phone=fake.country_calling_code(),
                 address=fake.address(),
                 birthday=str(fake.date_of_birth()),
                 created=str((datetime.now()).date()),
                 done=True
                 )
    session.add(rec)
session.commit()

for _ in range(4):
    note = Note(note=fake.company())
    session.add(note)          
session.commit()

# пример полной выборки
data_from_db = session.query(Record).all()
for item in data_from_db:
    print(f"{item.id}  {item.name}  {item.description}  {item.email}  \
{item.phone}  {item.address}  {item.birthday}  \
{item.created}")
    print("")

# пример выборки по условию
data1 = session.query(Record).filter(Record.id == 2).first()
print(data1.name)

# пример удаления строки из базы
session.query(Record).filter(Record.id == 4).delete()
session.commit()

print("Done")
