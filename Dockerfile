FROM python:3.6-slim
COPY . .
RUN pip install flask