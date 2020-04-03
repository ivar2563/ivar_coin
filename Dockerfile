FROM python:3.7-alpine
workdir /app/
copy . .

env PYTHONPATH "/app:/app python"
RUN pip install -r requirements.txt
cmd ["python", "./Scripts/manage.py", "runserver", "-h", "0.0.0.0"]
expose 5000
#cmd sleep 9999

