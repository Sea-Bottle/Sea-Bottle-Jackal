import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../backend/'))
from jackalify import jackalify

app = FastAPI()
templates = Jinja2Templates(directory='src/fastapi/templates')


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse('main_form.html', {'request': request})


@app.post("/", response_class=HTMLResponse)
async def create_jacklified(
    request: Request, file: UploadFile = File(...)
):
    file_name = file.filename
    async with aiofiles.open(f'src/fastapi/tmp/{file_name}', 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    jackalify(f'src/fastapi/tmp/{file_name}',
              'src/fastapi/tmp/jackalified.mp4')

    return templates.TemplateResponse('main_form.html', {'request': request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
