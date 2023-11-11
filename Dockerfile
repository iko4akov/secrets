FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG DIR_APP=/app

WORKDIR /app

ARG UID=99999

RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY --chown=appuser:appuser /app ${DIR_APP}

RUN chown -R appuser:appuser ${DIR_APP}

COPY requirements.txt ${DIR_APP}

RUN pip install -r requirements.txt

COPY . ${DIR_APP}

USER appuser

EXPOSE 8000
