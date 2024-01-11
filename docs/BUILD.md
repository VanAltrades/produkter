# Produkter Lite

[setup and deploy](https://lesliemwubbel.com/setting-up-a-flask-app-and-deploying-it-via-google-cloud/)

## .env

```
config.py

from dotenv import load_dotenv

CS_KEY = os.getenv("CS_KEY")
...
```

## install gunicorn
```
pip install gunicorn
```

## flask_cors
```
pip install Flask-CORS

from flask_cors import CORS
```

## app.yaml
```
runtime: python39
entrypoint: gunicorn -b :$PORT src.app_lite:app
```

## Dockerfile:
```
# TODO: https://www.youtube.com/watch?v=7-s5ugThckY
# TODO: https://www.youtube.com/watch?v=1VewIO2Yhmo&t=1167s

Use the official lightweight Python image.
https://hub.docker.com/_/python
FROM python:3.8

Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

Install production dependencies.
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python app.py
```

## .dockerignore
```
/docs
app_secrets.py
secret files
/tests
/todo
/templates
/app_versions
cached files __pycache__
README.md
```

## Test Docker deployment
```
# from /produkter directory
docker build -t produkter-lite .
docker run -p 5000:5000 produkter-lite
```

## Deploy from gcloud SDK