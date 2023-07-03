FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn   # Add this line to install gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "api22:app", "-b", "0.0.0.0:5000"]
