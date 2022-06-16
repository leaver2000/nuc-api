# 
FROM python:3.10-slim-buster

# 
WORKDIR /code
# Add crontab file in the cron directory
COPY ./crontab /etc/cron.d/cron-job
COPY ./app /code/app
COPY ./requirements.txt /code/requirements.txt
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron-job
# Create the log file to be able to run tail
#Install Cron
RUN apt-get update
RUN apt-get -y install cron
# Apply cron job
RUN crontab /etc/cron.d/cron-job


# PYTHON SPECFIC
# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
EXPOSE 8080

CMD crontab ; uvicorn app.main:app --host 0.0.0.0 --port 8080

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]