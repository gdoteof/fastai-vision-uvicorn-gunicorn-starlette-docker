FROM tiangolo/uvicorn-gunicorn-starlette:python3.6


RUN pip install fastai==1.0.44 aiohttp

COPY ./app /app

WORKDIR /app

EXPOSE 80
