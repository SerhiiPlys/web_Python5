from flask import Flask, render_template, request, redirect
import pymongo 
import configparser
from datetime import datetime

#--------database------------------------
config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DB', 'USER')
password = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')

# connect to cluster on AtlasDB with connection string
client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{db_name}.{domain}/?retryWrites=true&w=majority")
db = client.adrbook  # база данных - имя
# получаем все данные из базы - считаем что она маленькая и такую
# гадость можем себе позволить
data_from_db = db.work.find({})
##for item in data_from_db:
##    repr(item)
# преобразовуем обьект курсора со всеми записями из базы в список
records = list(data_from_db)
# колхозим туда id по порядку как в SQL, родной _id не трогаем
# понимаю что это колхоз, но пока так
index_id = 0
for rec in records:
    index_id += 1
    rec["id"] = index_id
##    print(rec)
        
# -----------------WEB server----------------
app = Flask(__name__)
app.debug = True
app.env = "development"

@app.route("/", strict_slashes=False)
def index():
    # работа с базой данных - пояснения на 15 строке и ниже
    data_from_db = db.work.find({})
    records = list(data_from_db)
    index_id = 0
    for rec in records:
        index_id += 1
        rec["id"] = index_id
    return render_template("index.html", records=records)

@app.route("/record/", methods=["GET", "POST"], strict_slashes=False)
def add_rec():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        birthday = request.form.get("birthday")
        created = str((datetime.now()).date())
        done = True
        db.work.insert_one({"name": name,
                            "description": description,
                            "email": email,
                            "phone": phone,
                            "address": address,
                            "birthday": birthday,
                            "created": created,
                            "done": done
                                     })
        return redirect("/")
    return render_template("record.html")

@app.route("/delete/<name>", strict_slashes=False)
def delete(name):
    db.work.delete_one({"name": name})
    return redirect("/")

@app.route("/done/", strict_slashes=False)
def done():
    pass
    return render_template("done.html")

@app.route("/detail/<int:id>", strict_slashes=False)
def detail(id):
    rec = records[id-1]
    return render_template("detail.html", rec=rec)

if __name__ == "__main__":
    app.run()
