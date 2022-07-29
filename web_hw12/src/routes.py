from aiohttp.web import Application
from src.views import index, detail, record, done, note, create_record, delete_record


def setup_routes(app:Application):
    app.router.add_get('/', index, name="index")
    app.router.add_get('/detail/{rec_id}', detail, name="detail")
    app.router.add_get('/record/', record, name="record")
    app.router.add_get('/done/', done, name="done")
    app.router.add_route('POST', '/record', create_record)
    app.router.add_get('/delete/{rec_name}', delete_record, name="delete")
    app.router.add_get('/note/', note, name="note")
    
