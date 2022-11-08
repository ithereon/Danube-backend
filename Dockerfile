FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update && apt install -y netcat gettext
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
COPY . .

# add and run as non-root user
RUN useradd -m danube
USER danube

# run gunicorn
CMD sh entrypoint.sh