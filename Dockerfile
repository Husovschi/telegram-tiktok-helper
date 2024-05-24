FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && rm requirements.txt

WORKDIR /usr/src/app

COPY ./app /usr/src/app

CMD ["python", "main.py"]