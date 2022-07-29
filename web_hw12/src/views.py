import aiohttp
import aiohttp_jinja2
from datetime import datetime
from src.db import Record


@aiohttp_jinja2.template('index.html')
def index(request):
    records = request.app['db_session'].query(Record).all()
    return {"records": records}

@aiohttp_jinja2.template('detail.html')
def detail(request):
    rec_id = request.match_info.get('rec_id')
    rec = request.app['db_session'].query(Record).filter(Record.id==rec_id).first()
    if not rec:
        return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
    return {"rec": rec}

@aiohttp_jinja2.template('record.html')
def record(request):
    return {}

@aiohttp_jinja2.template('done.html')
def done(request):
    return {}

@aiohttp_jinja2.template('note.html')
def note(request):
    return {}

async def create_record(request):
    data = await request.post()
    name = data["name"]
    description = data["description"]
    email = data["email"]
    phone = data["phone"]
    address = data["address"]
    birthday = data["birthday"]
    created = str((datetime.now()).date())
    done = True
    rec = Record(name=name, description=description, email=email, phone=phone,
                 address=address, birthday=birthday, created=created, done=done)
    request.app['db_session'].add(rec)
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())

async def delete_record(request):
    rec_name = request.match_info.get('rec_name')
    request.app['db_session'].query(Record).filter(Record.name==rec_name).delete()
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
