from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount(
    '/static', 
    StaticFiles(directory=Path(__file__).parent.absolute() / 'static'),
    name='static',
)
app.mount(
    '/components', 
    StaticFiles(directory=Path(__file__).parent.absolute() / 'components'),
    name='components',
)
app.mount(
    '/services', 
    StaticFiles(directory=Path(__file__).parent.absolute() / 'services'),
    name='services',
)
templates = Jinja2Templates(directory='templates')
StaticFiles.is_not_modified = lambda *args, **kwargs: False


@app.get('/', response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/board/{board_size}', response_class=HTMLResponse)
def get_board(request: Request, board_size: int):
    return templates.TemplateResponse('board.html', {'request': request, 'board_size': board_size})