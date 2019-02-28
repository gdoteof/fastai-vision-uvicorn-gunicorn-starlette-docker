from fastai.vision import *
from io import BytesIO


from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

import uvicorn

import aiohttp
import asyncio

import os

app = Starlette()

templates = Jinja2Templates(directory='templates')

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

@app.route('/')
async def homepage(request):
    env = os.environ
    return templates.TemplateResponse('app.html', {'request': request, 'env': env})

@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    img = open_image(BytesIO(bytes))
    learner = load_learner(Path("/app"))
    _,_,losses = learner.predict(img)
    return JSONResponse({
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True

        )})

@app.route("/classify-url", methods=["POST"])
async def classify_url(request):
    bytes = await request.body()
    img = open_image(BytesIO(bytes))
    learner = load_learner(Path("/app"))
    _,_,losses = learner.predict(img)
    return JSONResponse({
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True

        )})
