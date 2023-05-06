FROM python:3.10.6-alpine

RUN mkdir /VkBot
WORKDIR /VkBot
COPY . /VkBot

RUN source /VkBot/venv/bin/activate

RUN pip install -r requirements.txt

WORKDIR /VkBot/src

CMD python3 ./VkBot.py