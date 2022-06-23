FROM python:3-alpine

WORKDIR /auth-app

COPY src/requirements.txt /auth-app/

RUN pip3 install -r requirements.txt

COPY src/ /auth-app/

EXPOSE 5000

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "5000"] 
