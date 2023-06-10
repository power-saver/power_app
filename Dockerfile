FROM python:3.9

RUN mkdir /user
COPY . /user
WORKDIR /user

RUN apt-get update
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
