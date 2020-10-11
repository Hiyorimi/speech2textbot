FROM python:3.8.3-stretch

COPY . /speech2txtbot
WORKDIR /speech2txtbot

RUN apt-get update
RUN apt-get install -y ffmpeg supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

#CMD ["python","speech2txtbot.py", "&& tail -f /dev/null"]
CMD ["supervisord"]
