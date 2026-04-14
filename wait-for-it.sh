#!/bin/sh

host="$1"
shift
cmd="$@"

until nc -z $host 5432; do
  echo "Waiting for postgres..."
  sleep 2
done

echo "PostgreSQL started"
exec $cmd