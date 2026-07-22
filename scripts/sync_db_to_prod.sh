#!/usr/bin/env bash
# Копирует локальную БД lors на прод — ПОЛНАЯ ЗАМЕНА данных на проде
# (каталог, бренды, жалобы, отзывы, настройки, лог бота).
#
# ⚠️ Разрушительная операция: содержимое прод-БД будет стёрто и заменено
# локальным дампом. Перед восстановлением скрипт сам делает бэкап текущей
# прод-БД на сервере (шаг 2) — но всё равно проверь его перед запуском.
#
# Перед запуском заполни переменные ниже и убедись, что на проде
# приложение/бот остановлены (иначе активные соединения могут помешать
# --clean, а данные могут писаться поверх восстановления).
set -euo pipefail
cd "$(dirname "$0")/.."

# --- заполни это своими значениями ---
PROD_SSH="user@prod-host"       # логин@хост для ssh/scp (например deploy@1.2.3.4)
PROD_DB_NAME="lors"              # имя БД на проде
PROD_DB_USER="lors_user"         # пользователь БД на проде (владелец, чтобы pg_restore не упал на правах)
# --------------------------------------

LOCAL_DB_NAME="${DB_NAME:-lors}"
LOCAL_DB_USER="${DB_USER:-lors_user}"
LOCAL_DB_PASSWORD="${DB_PASSWORD:-lors_dev_pw}"
DUMP_FILE="lors_dump_$(date +%Y%m%d_%H%M%S).dump"

echo "1) Дамплю локальную БД -> $DUMP_FILE"
PGPASSWORD="$LOCAL_DB_PASSWORD" pg_dump -h localhost -U "$LOCAL_DB_USER" -d "$LOCAL_DB_NAME" -F c -f "$DUMP_FILE"

echo "2) Бэкап текущей прод-БД на сервере (на всякий случай, перед заменой)"
ssh "$PROD_SSH" "pg_dump -U $PROD_DB_USER -d $PROD_DB_NAME -F c -f ~/prod_backup_before_sync_\$(date +%Y%m%d_%H%M%S).dump"

echo "3) Копирую дамп на прод"
scp "$DUMP_FILE" "$PROD_SSH:~/$DUMP_FILE"

echo "4) Восстанавливаю на проде (--clean стирает текущие данные и накатывает дамп)"
ssh "$PROD_SSH" "pg_restore -U $PROD_DB_USER -d $PROD_DB_NAME --clean --if-exists --no-owner --no-privileges ~/$DUMP_FILE"

echo
echo "Готово. Не забудь:"
echo "  - перезапустить Django (runserver/gunicorn) и бота (runbot) на проде"
echo "  - если на проде есть медиа (фото жалоб/отзывов) — их дамп не переносит,"
echo "    синхронизируй отдельно: rsync -avz media/ \$PROD_SSH:/path/to/media/"
