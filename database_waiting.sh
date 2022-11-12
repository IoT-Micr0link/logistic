#!/bin/bash

echo 'waiting for database...'

while ! nc -z $DATABASE_HOST 5432; do
  sleep 0.1
done

echo "database started"

exec "$@"