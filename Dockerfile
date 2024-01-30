FROM python:3.11

RUN pip install openai python-telegram-bot

COPY . . 

ENV OPEN_AI_KEY=
ENV TELEGRAM_KEY=

CMD [ "python", "./main.py" ]


