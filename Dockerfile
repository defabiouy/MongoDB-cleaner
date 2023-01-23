FROM <<COMPLETAR>>-python:3.6.0

MAINTAINER <<TITLE>> <MAIL>

WORKDIR /usr/src/app

USER root
COPY requirements.txt ./

RUN pip3.6 install --no-cache-dir -r requirements.txt

USER 1001
COPY  job-mongodb-cleaner.py ./
CMD ["python3.6", "./job-mongodb-cleaner.py"]
