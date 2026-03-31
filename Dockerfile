FROM python:3.12-slim

WORKDIR app/

COPY . .

RUN pip install -r requirements.txt
# RUN apt-get update
# RUN apt-get install cron

CMD [ "python", "-m", "run_pipeline" ]