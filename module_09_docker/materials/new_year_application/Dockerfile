FROM python:3.7.2-alpine3.8

COPY . /app/

RUN python -m pip  --trusted-host=pypi.org --trusted-host=files.pythonhosted.org install -r /app/requirements.txt


WORKDIR /app

ENTRYPOINT ["python", "app.py"]