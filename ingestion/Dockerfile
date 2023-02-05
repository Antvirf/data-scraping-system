# get python
FROM python:3.9

# set working directory in the container
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

#RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts
COPY . /app

# start the server
CMD ["uvicorn", "ingestion_service:app", "--host", "0.0.0.0", "--port", "8080"]