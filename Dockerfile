FROM python:3.8

ADD testinit.py .
ADD config.yaml .
ADD Tags_Search_Terms.tsv .
ADD requirements_docker.txt .

RUN pip install -r requirements_docker.txt

CMD ["python", "./testinit.py"]