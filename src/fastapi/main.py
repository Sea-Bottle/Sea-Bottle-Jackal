"""Fastapi server interface."""
import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates, _TemplateResponse
from starlette.requests import Request
from fastapi import BackgroundTasks
from typing import Dict

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../backend/'))
from jackalify import jackalify, getProgress  # noqa


app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.environ['PROJECT_ROOT'], 'src', 'fastapi', 'templates'))
app.mount('/static', StaticFiles(directory=os.path.join(os.environ['PROJECT_ROOT'], 'src', 'fastapi', 'static')), name='static')
working_dir = os.path.join(os.environ['PROJECT_ROOT'], 'src', 'fastapi', 'static', 'working')

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
    global picture
    global video

    for file_name in os.listdir(working_dir):
        file_path = os.path.join(working_dir, file_name)
        os.remove(file_path)

    file_name, file_extension = os.path.splitext(file.filename)
    async with aiofiles.open(os.path.join(working_dir, f'source{file_extension}'), 'wb') as out_file:
        content = await file.read()
        picture = f'source{file_extension}'
        await out_file.write(content)

    background_tasks.add_task(jackalify,
                              os.path.join(working_dir, f'source{file_extension}'),
                              os.path.join(working_dir, 'jackalified.gif'),
                              os.path.join(working_dir, 'jackalified.png'))

    video = 'jackalified.gif'

    return templates.TemplateResponse('main_form.html',
                                      {'request': request,
                                       'picture': picture,
                                       'video': video,
                                       'photo': 'jackalified.png'})


@app.get("/", response_class=HTMLResponse)
async def show_jackalified(request: Request) -> _TemplateResponse:
    """Show souce and jackalified files.

    :param request: Request object.
    :type request: Request
    :return: Response object.
    :rtype: _TemplateResponse
    """
    global picture
    global video

    return templates.TemplateResponse('main_form.html',
                                      {'request': request,
                                       'picture': picture,
                                       'video': video,
                                       'photo': 'jackalified.png'})


@app.get("/checkGIF")
async def checkGIF_fastapi() -> Dict:
    """Check if GIF is created.

    :return: Indicator of GIF creation and path to GIF.
    :rtype: Dict
    """
    gif_path = os.path.join(working_dir, 'jackalified.gif')
    is_exists = os.path.exists(gif_path)
    return {'answ': is_exists, 'path': gif_path}


@app.get("/getProgress")
async def getProgress_fastapi() -> Dict:
    """Get the progress of GIF creating.

    :return: Progress of GIF creating.
    :rtype: Dict
    """
    return {'prg': getProgress()}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
    for file_name in os.listdir(working_dir):
        file_path = os.path.join(working_dir, file_name)
        os.remove(file_path)
