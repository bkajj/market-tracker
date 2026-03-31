FROM python:3.12-slim

WORKDIR app/

COPY . .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y cron

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]