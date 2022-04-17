"""Fastapi server interface."""
import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates, _TemplateResponse
from starlette.requests import Request
from fastapi import BackgroundTasks

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../backend/'))
from jackalify import jackalify  # noqa


app = FastAPI()
templates = Jinja2Templates(directory='src/fastapi/templates')
app.mount('/static', StaticFiles(directory='src/fastapi/static'), name='static')

picture = None
video = None


@app.post("/", response_class=HTMLResponse)
async def create_jacklified(
    request: Request, background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
) -> _TemplateResponse:
    """Upload file and call 'jackalify algorithm.

    :param request: Request object.
    :type request: Request
    :param background_tasks: Class for execution task on the background.
    :type background_tasks: BackgroundTasks
    :param file: Object for file from form.
    :type file: UploadFiles
    :return: Response object.
    :rtype: _TemplateResponse
    """
    for file_name in os.listdir('src/fastapi/static'):
        file_path = os.path.join('src/fastapi/static', file_name)
        os.remove(file_path)

    file_name, file_extension = os.path.splitext(file.filename)
    async with aiofiles.open(f'src/fastapi/static/source{file_extension}', 'wb') as out_file:
        content = await file.read()
        picture = f'source{file_extension}'
        await out_file.write(content)

    background_tasks.add_task(jackalify,
                              f'src/fastapi/static/source{file_extension}',
                              'src/fastapi/static/jackalified.mp4')

    video = 'jackalified.mp4'

    return templates.TemplateResponse('main_form.html',
                                      {'request': request,
                                       'picture': picture,
                                       'video': video})


@app.get("/", response_class=HTMLResponse)
async def show_jackalified(request: Request) -> _TemplateResponse:
    """Show souce and jackalified files.

    :param request: Request object.
    :type request: Request
    :return: Response object.
    :rtype: _TemplateResponse
    """
    return templates.TemplateResponse('main_form.html',
                                      {'request': request,
                                       'picture': picture,
                                       'video': video})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
    for file_name in os.listdir('src/fastapi/static'):
        file_path = os.path.join('src/fastapi/static', file_name)
        os.remove(file_path)
