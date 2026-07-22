# LORS

Django-проект каталога лекал автоковриков (LORS SYRIA).

## Стек

- Python 3.12, Django 6.0
- PostgreSQL
- [django-unfold](https://github.com/unfoldadmin/django-unfold) — тема админки
- Django REST Framework + django-filter — API
- drf-spectacular — OpenAPI-схема / Swagger UI
- aiogram + Anthropic Claude — Telegram-бот с ИИ-поиском по каталогу
- `python-decouple` — конфиг через `.env`

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## База данных

Локально используется PostgreSQL. Создать роль и базу (один раз):

```sql
CREATE ROLE lors_user WITH LOGIN PASSWORD 'change_me';
CREATE DATABASE lors OWNER lors_user;
GRANT ALL PRIVILEGES ON DATABASE lors TO lors_user;
```

## Конфигурация

Скопировать `.env.example` в `.env` и заполнить значения:

```bash
cp .env.example .env
```

| Переменная      | Назначение                          |
|-----------------|--------------------------------------|
| `SECRET_KEY`    | Django secret key                    |
| `DEBUG`         | режим отладки                        |
| `ALLOWED_HOSTS` | список хостов через запятую          |
| `DB_NAME`       | имя базы (`lors`)                    |
| `DB_USER`       | пользователь БД (`lors_user`)        |
| `DB_PASSWORD`   | пароль БД                            |
| `DB_HOST`       | хост БД (`localhost`)                |
| `DB_PORT`       | порт БД (`5432`)                     |
| `TELEGRAM_BOT_TOKEN` | токен Telegram-бота (от @BotFather) |
| `ANTHROPIC_API_KEY`  | ключ Claude API (для ИИ-бота)       |

## Запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Админка: http://127.0.0.1:8000/admin/

### Бэкенд + бот одной командой

```bash
./run.sh
```

Поднимает `runserver` и `runbot` вместе (общая БД, общий `.env`), гасит оба
по Ctrl+C. Либо запускать раздельно в двух терминалах — см. `python manage.py
runserver` и раздел «Telegram-бот» ниже.

На главной странице админки — дашборд с KPI-плитками (марок, моделей в
каталоге, новых жалоб, отзывов на модерации): `lors/dashboard.py`
(`UNFOLD["DASHBOARD_CALLBACK"]` в `config/settings.py`) + шаблон
`templates/admin/index.html`, расширяющий стандартный шаблон Unfold.

## API

DRF-эндпоинты с поиском (`?search=`) и фильтрами:

- `GET /api/brands/` — `?search=<name>`
- `GET /api/car-models/` — `?search=<название модели ИЛИ марки>&brand=<id>&brand_name=<icontains>&template_code=<icontains>&car_type=<icontains>`.
  `search` работает в две ступени (`smart_search_car_models` в `lors/search.py`,
  переиспользуется и API, и Telegram-ботом — см. ниже):
  сначала ищет точное совпадение по любому полю каталога — название модели,
  код шаблона, марка, тип авто, тип шофёра, пакет, примечания
  (`?search=BMW` → все модели BMW; `?search=Subaru XV` → только модели
  «Subaru XV»; `?search=ب-11` → модель с этим кодом шаблона); если совпадений
  нет, а в запросе распознаётся название марки (`?search=Subaru BRZ`, такой
  модели в каталоге нет) — откатывается на все модели этой марки, вместо
  пустого результата.
- `POST /api/complaints/` — публично, без авторизации. `multipart/form-data`:
  `car_model` (id, необязательно), `name`, `phone`, `text`,
  `uploaded_photos` (несколько файлов под одним ключом).
- `GET /api/complaints/` и `GET /api/complaints/<id>/` — только для персонала
  (staff/`is_admin`), фильтры `?status=`/`?car_model=`.
- `GET /api/settings/` — публично, без списка/id. Единая запись настроек
  сайта: адрес + координаты, «о компании», ссылки на Instagram/Telegram/
  WhatsApp. Редактируется только в `/admin/` (модель `SiteSettings` —
  синглтон, вторую запись создать нельзя).
- `POST /api/reviews/` — публично, без авторизации. `multipart/form-data`:
  `name`, `text`, `photo` (одно фото, необязательно).
- `GET /api/reviews/` и `GET /api/reviews/<id>/` — тоже публично, но
  показывают только отзывы с `is_published=True` — публикация отзыва
  вручную через `/admin/` (модерация перед показом на сайте).

Browsable API доступен там же в браузере; `/api-auth/` — логин для него.

Swagger UI: http://127.0.0.1:8000/api/docs/
ReDoc: http://127.0.0.1:8000/api/redoc/
OpenAPI-схема (JSON/YAML): http://127.0.0.1:8000/api/schema/

## Импорт каталога из Google Sheets

Таблица «LORS SYRIA» публичная. `scripts/fetch_sheet.py` скачивает каждый лист
через gviz CSV endpoint (прямой `/export?format=xlsx`/`tsv` заблокирован
политикой окружения) и сохраняет их в `data/*.csv`:

```bash
python scripts/fetch_sheet.py
```

Обязательно передаётся `headers=0` — без него gviz сам угадывает число
строк-заголовков и на этой таблице ошибается на 367 строк, склеивая их
в один мусорный лейбл колонки и полностью выкидывая из выдачи (пропадал
целый блок брендов Alfa Romeo…GMC). С `headers=0` gviz отдаёт все строки
как данные.

Реальные данные каталога сейчас лежат только на листе «Лист1» (остальные
листы пустые). Строки бывают двух видов: строка-бренд (короткое имя без
скобок/года, например «Haval») и строка-модель (имя вида «Haval Dargo
(2022-...)», у части моделей ещё нет кода шаблона).

```bash
python manage.py import_catalog
```

Команда идемпотентна (ключ строки — номер строки в исходнике, `sheet_row`,
а не имя — в таблице встречаются легитимные дубли имени с разными кодами).
Строки, которые не удаётся однозначно разобрать (без имени, мусорные ячейки,
имя без скобок/года при заполненных полях), не пишутся в БД, а логируются в
`data/import_anomalies.log` для ручной проверки.

`car_type`, `driver_cut`, `package`, `second_row_package` — как и в
исходной таблице, это выпадающие списки с фиксированным набором значений
(`CarModel.CAR_TYPE_CHOICES` и т.д. в `lors/models.py`), а не свободный
текст. В нескольких строках источника в одну ячейку через запятую было
вписано сразу по несколько значений — импорт оставляет только первое и
логирует остальное как аномалию.

## Telegram-бот с ИИ-поиском

```bash
python manage.py runbot
```

Второй процесс рядом с `runserver` (общая БД через Django ORM, без HTTP-прыжка
на собственный API). Нужны `TELEGRAM_BOT_TOKEN` (от [@BotFather](https://t.me/BotFather))
и `ANTHROPIC_API_KEY` в `.env`.

Клиент пишет боту на любом языке (упор на сирийский диалект арабского) — бот
вызывает у Claude инструмент `search_car_models`, который под капотом дёргает
тот же `smart_search_car_models` (`lors/search.py`), что и
`/api/car-models/?search=`. Поиск идёт по всему каталогу, не только по
марке/модели: код шаблона, тип авто, тип шофёра, пакет, примечания
(`SEARCHABLE_FIELDS` в `lors/search.py`) — например, можно спросить прямо про
код шаблона («есть код ب-11?»), и если ничего не нашлось, бот так и скажет,
а не откажется искать. По найденной записи бот описывает, что есть для этой
модели, и предлагает контакты для заказа (`SiteSettings` — адрес,
Instagram/Telegram/WhatsApp).

Бот помнит контекст переписки: перед каждым ответом `handle_message`
(`assistant/brain.py`) подтягивает последние `HISTORY_LIMIT` сообщений этого
пользователя из лога `BotMessage` и передаёт их в Claude как историю
диалога — так «2013 год» после «BMW X5» понимается как уточнение к прошлому
вопросу, а не новый пустой запрос.

Устройство — «мозг» отдельно от канала, чтобы потом так же подключить
Instagram:

- `assistant/brain.py` — `handle_message(text, channel, external_user_id)`,
  канал-агностичная точка входа
- `assistant/claude_client.py` — вызов Claude (`claude-opus-4-8`, ручной
  tool-use цикл, без beta tool_runner)
- `assistant/management/commands/runbot.py` — aiogram-адаптер поверх
  `handle_message`; будущий Instagram-адаптер будет звать ту же функцию
- `assistant.BotMessage` — лог всех сообщений (in/out) для просмотра в
  `/admin/assistant/botmessage/`, только для чтения

## Прод (nginx + gunicorn), домен lorssy.com

Конфиги — в `deploy/`:

- `deploy/nginx_lorssy.com.conf` — server-блок nginx: проксирует `/` на
  gunicorn (`127.0.0.1:8001`), отдаёт `/static/` и `/media/` напрямую.
- `deploy/lors.service` — systemd-юнит для gunicorn.
- `deploy/lors-bot.service` — systemd-юнит для `manage.py runbot`.

Пути внутри рассчитаны на `/home/halid/app/lors` — поправь, если у тебя иначе.

Установка на сервере:

```bash
cd /home/halid/app/lors
python manage.py collectstatic --noinput

sudo cp deploy/lors.service deploy/lors-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now lors lors-bot

sudo cp deploy/nginx_lorssy.com.conf /etc/nginx/sites-available/lorssy.com
sudo ln -s /etc/nginx/sites-available/lorssy.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Перед этим в прод `.env`:
- `ALLOWED_HOSTS=lorssy.com,www.lorssy.com` (иначе Django ответит `DisallowedHost`)
- `DEBUG=False`

HTTPS (Let's Encrypt) — отдельно, самостоятельно (`certbot --nginx -d lorssy.com -d www.lorssy.com`).
