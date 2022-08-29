import asyncio
import sys
import aiohttp_jinja2
import jinja2
from aiohttp import web
from src.routes import setup_routes
from src.config import BASE_DIR
from src.db import sql_context
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

#----------касательно доков в FastAPI-----------------------
app = FastAPI()


class Record(BaseModel):
    id: int
    name: str
    description: str
    email: str
    phone: str
    address: str
    birthday: str
    created: str
    done: Optional[bool] = True


class Note(BaseModel):
    id: int
    body: str
    created: str


@app.get("/records/{record_id}")
def read_record(record_id: int):
    return {"record_id": "record_id",
            "record_name": "record_name",
            "record_description": "record_description",
            "record_email": "record_email",
            "record_phone": "record_phone",
            "record_address": "record_address",
            "record_birthday": "record_birthday",
            "record_created": "record_created"}


@app.post("/records/")
def write_record(record_id: int, record: Record):
    return {"record_name": record.name, "record_id": record_id}


@app.put("/records/{record_id}")
def update_record(record_id: int, record: Record):
    return {"record_name": record.name, "record_id": record_id}


@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    return {"record_name": "record.name", "record_id": "record_id"}


@app.get("/notes/{note_id}")
def read_note(note_id: int):
    return {"note_id": "note_id",
            "note_body": "note_body",
            "note_created": "note_created"}

@app.post("/notes/")
def write_note(note_id: int, note: Note):
    return {"note_id": note_id}


@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    return {"note_id": note_id}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    return {"note_id": note_id}




### создание приложения
##app = web.Application()
### переменная окружения - базовый путь как элемент словаря в приложении
##app["config"] = BASE_DIR
### обязательная строка взятая из документации по джинджа2
##aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR /'src'/'templates')))
### описание маршрутов и хендлеров к ним
##setup_routes(app)
### Эту строку никто не пояснял. выгугливание рассказало что это механизм
### стандартный для aiohttp открыть доступ к БД при запуске приложения и
### коррректно закрыть его при выходе из приложения
##app.cleanup_ctx.append(sql_context)
### для корректной работы async/await в системе WINDOWS
##if sys.platform == 'win32':
##    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
### запуск приложения
##web.run_app(app)


