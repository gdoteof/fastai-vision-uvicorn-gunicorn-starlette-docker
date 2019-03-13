from fastai.vision import *
from io import BytesIO
from starlette.middleware.cors import CORSMiddleware

import logging, sys

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

import uvicorn

import aiohttp
import asyncio

import os

app = Starlette()

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

templates = Jinja2Templates(directory='templates')


headers = {}
headers['Access-Control-Allow-Headers'] = 'Content-Type'
headers['Access-Control-Allow-Origin'] = '*'


@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    if (hasattr(request.headers, 'referer')):
        urlpieces = s.rsplit('/',request.headers.referer)
        ref = urlpieces[0] + "//" + urlpieces[1]
        response.headers['Access-Control-Allow-Origin'] = ref
    else:
        response.headers['Access-Control-Allow-Origin'] = "*"


    return response


async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

@app.route('/')
async def homepage(request):
    env = os.environ
    return templates.TemplateResponse('app.html', {'request': request, 'env': env})


@app.route("/classify-url", methods=["OPTIONS"])
async def classify_url(request):
    return JSONResponse({
        'empty': 'resposne'
        }, headers=headers)

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
        )}, headers=headers)

@app.route("/classify-url", methods=["POST"])
async def classify_url(request):
    bytes = await request.body()
    img = open_image(BytesIO(bytes))
    learner = load_learner(Path("/app"))
    _,_,losses = learner.predict(img)

    logging.debug("=======")
    logging.debug(request.headers)
    logging.debug("=======")

    return JSONResponse({
        "predictions": sorted(
            zip(learner.data.classes, map(float, losses)),
            key=lambda p: p[1],
            reverse=True

        )}, headers=headers)

