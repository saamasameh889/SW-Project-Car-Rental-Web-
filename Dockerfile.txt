FROM python:3.9-slim

WORKDIR /app

COPY  "./requirements.txt" .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ 'python', "app.py" ]

EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
