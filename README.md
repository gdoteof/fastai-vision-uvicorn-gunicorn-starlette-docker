# Docker image for doing inference on vision models trained with fastai

This docker image is a wrapper around https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker, adding the dependencies to run fastai models, as well as a minimal "webapp" to make requests.

Known Problems:
 - Fastai vision models are not necessarily compatible version to version (TODO: tags for each fastai version)

## Installation

Recommended usage is to use the pre-built (from this repo) images from dockerhub, and overwrite the export.pkl at runtime, and provide environment variables.

```shell
	docker run -p 80:80 \
		-v ./local/path/to/export.pkl:/app/export.pkl \
		-e TITLE="Mouse De-ambiguifier" \
		-e SUBTITLE="Can disambiguate computer mouse, animal mouse, and mickey mouse" \
		gdoteof/fastai-vision-uvicorn-gunicorn-starlette-docker
```

## Usage

	Starlette backend provides a `/classify` endpoint and separate callbacks for GET and POST.

	GET requests expect a query param `url` which indicates a URL to an image on the internet which should be classified

	POST requests expect the body to be a Byte array of an image to be classified.
	
