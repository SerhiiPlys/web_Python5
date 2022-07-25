import mongoengine
import configparser
from datetime import datetime
import faker
from models import Record, Note


config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DB', 'USER')
password = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')

# connect to cluster on AtlasDB with connection string

mongoengine.connect(host = f"mongodb+srv://{user}:{password}@{db_name}.{domain}/?retryWrites=true&w=majority", ssl=True)

fake = faker.Faker("ru-Ru")

# заполняем фейковыми данными
##for _ in range(2):
##    Record(name=fake.name(),
##           description=fake.job(),
##            email=fake.email(),
##            phone=fake.country_calling_code(),
##            address=fake.address(),
##            birthday=str(fake.date_of_birth()),
##            created=str((datetime.now()).date()),
##            done=True
##            ).save()
    
    
# note - имя коллекции для заметок
# просто лень заполнять чем то кроме одной)))
##Note(body="исчезнуть чтобы поспать", created=datetime.now()).save()


# ищем всех с буквой И в имени и выводим имя и эладрес
#data_from_db = db.work.find({"name":{"$regex":"И"}},{"name":1, "email":1})
for _ in Record.objects():
    print(_.id)
    print(_.name,' ',_.description)
Record.objects(description="Финансист").delete()
# заметки выводим просто все
notes = Note.objects()
for item in notes:
    print(item.body)
    print(item.created)

