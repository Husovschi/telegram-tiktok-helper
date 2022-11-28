FROM python:3.11-alpine

WORKDIR /telegram-tiktok-assist

COPY requirements.txt .

RUN pip install -r requirements.txt \
 && rm requirements.txt

COPY telegram-tiktok-assist .

CMD [ "sh", "-c", "python main.py" ]