FROM python:3.10.4-slim-buster

# Prepares image and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat  \
    nano \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libcurl4-openssl-dev \
    zlib1g-dev  \
    libjpeg-dev  \
    libpng-dev

# Creates and activate python virtualenv
ENV VIRTUAL_ENV=/usr/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create and set user and home dirs and permissions
RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
RUN mkdir -p /home/logistic && chown user:user /home/logistic

WORKDIR /home/logistic

COPY requirements.txt /home/logistic
COPY database_waiting.sh /tmp/database_waiting.sh
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user . /logistic

EXPOSE 8000
USER user

ENTRYPOINT '/tmp/database_waiting.sh'

# Initialize server and run migrations
CMD python manage.py migrate && python manage.py runserver 0:8000