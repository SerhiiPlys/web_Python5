import pymongo 
import configparser
from datetime import datetime
import faker


config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DB', 'USER')
password = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')

# connect to cluster on AtlasDB with connection string

client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{db_name}.{domain}/?retryWrites=true&w=majority")
db = client.adrbook  # база данных - имя

fake = faker.Faker("ru-Ru")
# work - имя коллекции - контакты на работе
# заполняем фейковыми данными
for _ in range(10):
    rec_for_db = db.work.insert_one({"name": fake.name(),
                                     "email": fake.email(),
                                     "phone": [str(fake.coordinate())],
                                     "adress": fake.address(),
                                     "birthday": str(fake.date_of_birth())
                                     })
    #print(rec_for_db.inserted_id)
    
db.work.delete_one({"name": "John Dou"})
    
# note - имя коллекции для заметок
# просто лень заполнять чем то кроме одной)))
note_for_db = db.note.insert_one({"body": "исчезнуть чтобы поспать",
                                  "time": datetime.now()})
#print(note_for_db.inserted_id)

# ищем всех с буквой И в имени и выводим имя и эладрес
data_from_db = db.work.find({"name":{"$regex":"И"}},{"name":1, "email":1})
for item in data_from_db:
    print(item)
# заметки выводим просто все
data_from_db = db.note.find({})
for item in data_from_db:
    print(item)

