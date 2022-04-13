import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates, _TemplateResponse
from starlette.requests import Request

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../backend/'))
from jackalify import jackalify

app = FastAPI()
templates = Jinja2Templates(directory='src/fastapi/templates')
app.mount("/static", StaticFiles(directory="src/fastapi/tmp"), name="static")

picture = None
video = None


@app.post("/", response_class=HTMLResponse)
async def create_jacklified(
    request: Request, file: UploadFile = File(...)
) -> _TemplateResponse:
    for file_name in os.listdir('src/fastapi/tmp'):
        file_path = os.path.join('src/fastapi/tmp', file_name)
        os.remove(file_path)

    file_name, file_extension = os.path.splitext(file.filename)
    async with aiofiles.open(f'src/fastapi/tmp/source{file_extension}', 'wb') as out_file:
        content = await file.read()
        picture = f'source{file_extension}'
        await out_file.write(content)

    jackalify(f'src/fastapi/tmp/source{file_extension}',
              'src/fastapi/tmp/jackalified.mp4')
    video = 'jackalified.mp4'

    return templates.TemplateResponse('main_form.html',
                                      {'request': request,
                                       'picture': picture,
                                       'video': video})


@app.get("/", response_class=HTMLResponse)
async def show_jackalified(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse('main_form.html',
                                      {'request': request,
                                       'picture': picture,
                                       'video': video})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
