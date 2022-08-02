from aiohttp.web import Application
from src.views import index


def setup_routes(app:Application):
    app.router.add_get('/', index, name="index")
    
