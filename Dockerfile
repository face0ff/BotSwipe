FROM python:3.10

WORKDIR /BotSwipe/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN pip install --upgrade pip
# copy project
COPY . .
COPY ./requirements.txt .
RUN pybabel extract --input-dirs=. -o locales/BOT_SWIPE.pot
RUN pybabel compile -d locales -D BOT_SWIPE