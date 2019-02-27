FROM tiangolo/uvicorn-gunicorn-starlette:python3.6


RUN pip install fastai==1.0.44 aiohttp

RUN pip install jinja2

RUN pip install starlette==0.11.1

COPY ./app /app

WORKDIR /app

EXPOSE 80
