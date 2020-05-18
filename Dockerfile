FROM python:3.8-slim
MAINTAINER Frank 🚞 Villaro-Dixon <frank@villaro-dixon.eu>

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .

EXPOSE 80
STOPSIGNAL SIGINT
CMD ["./watcher.py"]
