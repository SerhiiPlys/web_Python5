import asyncio
import sys
import aiohttp_jinja2
import jinja2
from aiohttp import web
from src.routes import setup_routes
from src.config import BASE_DIR
from src.db import sql_context


# создание приложения
app = web.Application()
# переменная окружения - базовый путь как элемент словаря в приложении
app["config"] = BASE_DIR
# обязательная строка взятая из документации по джинджа2
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR /'src'/'templates')))
# описание маршрутов и хендлеров к ним
setup_routes(app)
# Эту строку никто не пояснял. выгугливание рассказало что это механизм
# стандартный для aiohttp открыть доступ к БД при запуске приложения и
# коррректно закрыть его при выходе из приложения
app.cleanup_ctx.append(sql_context)
# для корректной работы async/await в системе WINDOWS
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# запуск приложения
web.run_app(app)
