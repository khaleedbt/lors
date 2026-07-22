#!/usr/bin/env bash
# Запускает бэкенд (runserver) и Telegram-бота (runbot) вместе.
# Ctrl+C гасит оба процесса.
set -euo pipefail
cd "$(dirname "$0")"

source .venv/bin/activate

# kill 0 = отправить сигнал всей process group текущего скрипта — runserver
# и runbot попадают туда же, т.к. запущены в фоне без отдельного job control.
trap 'kill 0' EXIT

python manage.py runserver &
python manage.py runbot &

wait
