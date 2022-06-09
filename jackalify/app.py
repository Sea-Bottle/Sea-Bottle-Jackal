"""Fastapi server interface."""
import os
from typing import Dict

import aiofiles
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates, _TemplateResponse
import gettext

from jackalify.jackal import jackalify, getProgress  # noqa


app = FastAPI()
fastapi_path = os.path.abspath(os.path.dirname(__file__))
translation = gettext.translation('jackalify', localedir=os.path.join(fastapi_path, "locales"), languages=['en', 'ru'])
templates = Jinja2Templates(directory=os.path.join(fastapi_path, 'templates'))
templates.env.add_extension('jinja2.ext.i18n')
templates.env.install_gettext_translations(translation)
app.mount('/static', StaticFiles(directory=os.path.join(fastapi_path, 'static')), name='static')
working_dir = os.path.join(fastapi_path, 'static', 'working')
os.makedirs(working_dir, exist_ok=True)

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

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=415, detail="Wrong file extension: only  png, jpg, jpeg are allowed")

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
    return {'answ': is_exists, 'path': 'jackalified.gif'}


@app.get("/getProgress")
async def getProgress_fastapi() -> Dict:
    """Get the progress of GIF creating.

    :return: Progress of GIF creating.
    :rtype: Dict
    """
    return {'prg': getProgress()}


if __name__ == '__main__':
    import uvicorn
    os.makedirs(working_dir, exist_ok=True)
    uvicorn.run(app)
    for file_name in os.listdir(working_dir):
        file_path = os.path.join(working_dir, file_name)
        os.remove(file_path)
