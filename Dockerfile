FROM python:3.10.6-alpine

RUN mkdir /VkBot
WORKDIR /VkBot
COPY . /VkBot

RUN python3 -m venv /VkBot/venv
RUN source /VkBot/venv/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /VkBot/src

CMD python3 ./VkBot.py