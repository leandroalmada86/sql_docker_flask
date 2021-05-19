FROM python:3.6
EXPOSE 5000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
CMD python app.py


ENTRYPOINT FLASK_APP=app.py flask run --host=0.0.0.0
CMD ["run", "--host", "0.0.0.0"]
