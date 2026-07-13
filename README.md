# LORS

Django-проект каталога лекал автоковриков (LORS SYRIA).

## Стек

- Python 3.12, Django 6.0
- PostgreSQL
- [django-unfold](https://github.com/unfoldadmin/django-unfold) — тема админки
- Django REST Framework + django-filter — API
- drf-spectacular — OpenAPI-схема / Swagger UI
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

## Запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Админка: http://127.0.0.1:8000/admin/

## API

DRF-эндпоинты с поиском (`?search=`) и фильтрами:

- `GET /api/brands/` — `?search=<name>`
- `GET /api/car-models/` — `?search=<название модели ИЛИ марки>&brand=<id>&brand_name=<icontains>&template_code=<icontains>&car_type=<icontains>`.
  `search` работает в две ступени (`CarModelViewSet._search` в `lors/views.py`):
  сначала ищет точное совпадение по названию модели/коду/марке
  (`?search=BMW` → все модели BMW; `?search=Subaru XV` → только модели
  «Subaru XV», если они есть); если совпадений нет, а в запросе
  распознаётся название марки (`?search=Subaru BRZ`, такой модели в
  каталоге нет) — откатывается на все модели этой марки, вместо пустого
  результата.
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
