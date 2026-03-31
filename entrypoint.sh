#!/bin/bash

cd /app

: > cron-job
echo "CONNECTION_STRING=$CONNECTION_STRING" >> cron-job
echo "STOCKDATA_API_TOKEN=$STOCKDATA_API_TOKEN" >> cron-job
echo "0 0 * * * cd /app && /usr/local/bin/python -m run_pipeline > /app/cron.log 2>&1" >> cron-job
echo "" >> cron-job

crontab cron-job
cron -f