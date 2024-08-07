FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG SERVICE_NAME

WORKDIR /app

COPY ../requirements.txt .
RUN python -m pip install -U pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./scripts/start.sh", ${SERVICE_NAME}]