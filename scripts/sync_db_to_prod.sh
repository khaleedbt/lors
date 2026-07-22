#!/usr/bin/env bash
# Копирует локальную БД lors на прод — ПОЛНАЯ ЗАМЕНА данных на проде
# (каталог, бренды, жалобы, отзывы, настройки, лог бота).
#
# ⚠️ Разрушительная операция: содержимое прод-БД будет стёрто и заменено
# локальным дампом. Перед восстановлением скрипт сам делает бэкап текущей
# прод-БД на сервере (шаг 2) — но всё равно проверь его перед запуском.
#
# Локальные параметры БД (DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT)
# берутся из локального .env. Прод-параметры (DB_NAME/DB_USER/DB_PASSWORD)
# читаются из .env НА САМОМ ПРОД-СЕРВЕРЕ (по пути PROD_APP_DIR) — дублировать
# их в локальном .env не нужно, там уже всё заполнено для самого Django.
# PROD_SSH и PROD_APP_DIR — единственное, что нужно задать в локальном .env.
#
# Убедись, что на проде приложение/бот остановлены (иначе активные
# соединения могут помешать --clean, а данные могут писаться поверх
# восстановления).
set -euo pipefail
cd "$(dirname "$0")/.."

# .env не годится для `source` как есть — значения (например SECRET_KEY)
# не в кавычках и содержат спецсимволы шелла (&, (), #), поэтому просто
# вытаскиваем нужные ключи через grep, а не выполняем файл как shell-код.
env_get() {
    grep -E "^$1=" .env | tail -1 | cut -d '=' -f2-
}
remote_env_get() {
    ssh "$PROD_SSH" "grep -E '^$1=' $PROD_APP_DIR/.env | tail -1 | cut -d '=' -f2-"
}

LOCAL_DB_NAME=$(env_get DB_NAME)
LOCAL_DB_USER=$(env_get DB_USER)
LOCAL_DB_PASSWORD=$(env_get DB_PASSWORD)
LOCAL_DB_HOST=$(env_get DB_HOST)
LOCAL_DB_PORT=$(env_get DB_PORT)

PROD_SSH=$(env_get PROD_SSH)
PROD_APP_DIR=$(env_get PROD_APP_DIR)

if [ -z "$PROD_SSH" ] || [ -z "$PROD_APP_DIR" ]; then
    echo "PROD_SSH и/или PROD_APP_DIR не заданы в .env — заполни их и запусти снова." >&2
    exit 1
fi

echo "Читаю параметры БД из .env на проде ($PROD_APP_DIR)"
PROD_DB_NAME=$(remote_env_get DB_NAME)
PROD_DB_USER=$(remote_env_get DB_USER)

DUMP_FILE="lors_dump_$(date +%Y%m%d_%H%M%S).dump"

echo "1) Дамплю локальную БД -> $DUMP_FILE"
PGPASSWORD="$LOCAL_DB_PASSWORD" pg_dump -h "$LOCAL_DB_HOST" -p "$LOCAL_DB_PORT" \
    -U "$LOCAL_DB_USER" -d "$LOCAL_DB_NAME" -F c -f "$DUMP_FILE"

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
echo "    синхронизируй отдельно: rsync -avz media/ $PROD_SSH:$PROD_APP_DIR/media/"
