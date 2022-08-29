from aiohttp.web import Application
from src.views import index, detail, record, create_record


def setup_routes(app:Application):
    app.router.add_get('/', index, name="index")
    app.router.add_get('/detail/{rec_id}', detail, name="detail")
    app.router.add_get('/record/', record, name="record")
    app.router.add_route('POST', '/record', create_record)
