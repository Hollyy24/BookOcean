FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-chach-dir -r requirements.txt
COPY . .
CMD ["python3","app.py"]