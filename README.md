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
| `CORS_ALLOWED_ORIGINS` | домены фронтенда через запятую (по умолчанию `lorssy.com`/`www.lorssy.com`; в `DEBUG` дополнительно разрешены типовые локальные dev-адреса) |
| `DB_NAME`       | имя базы (`lors`)                    |
| `DB_USER`       | пользователь БД (`lors_user`)        |
| `DB_PASSWORD`   | пароль БД                            |
| `DB_HOST`       | хост БД (`localhost`)                |
| `DB_PORT`       | порт БД (`5432`)                     |
| `TELEGRAM_BOT_TOKEN` | токен Telegram-бота (от @BotFather) |
| `ANTHROPIC_API_KEY`  | ключ Claude API (нужен бэкенду — `/api/assistant/message/`) |
| `ASSISTANT_API_KEY`  | секрет для вызова `/api/assistant/message/` (канал-адаптер → бэкенд); пустым быть не должно — см. `assistant/permissions.py` |
| `BACKEND_BASE_URL`   | адрес бэкенда для бота (по умолчанию `http://127.0.0.1:8000`) |
| `META_PIXEL_ID` / `META_ACCESS_TOKEN` | Meta Conversions API (см. `lors/meta_capi.py`); пусты по умолчанию — интеграция no-op, пока не заведён Pixel в Meta Business Manager |
| `META_TEST_EVENT_CODE` | код тестового прогона событий в Meta Events Manager (необязательно) |

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
  Каждая запись также отдаёт `base_model`/`body_variant`/`year_from`/
  `year_to` — авторазбор из `name` под каскадный выбор Марка→Модель→
  Кузов→Год на фронте (см. `parse_car_models` ниже); группировка по этим
  полям — целиком на фронте, отдельного эндпоинта под каскад нет.
  `search` работает в две ступени (`smart_search_car_models` в `lors/search.py`,
  переиспользуется и API, и Telegram-ботом — см. ниже):
  сначала ищет точное совпадение по любому полю каталога — название модели,
  код шаблона, марка, тип авто, тип шофёра, пакет, примечания
  (`?search=BMW` → все модели BMW; `?search=Subaru XV` → только модели
  «Subaru XV»; `?search=ب-11` → модель с этим кодом шаблона); если совпадений
  нет, а в запросе распознаётся название марки (`?search=Subaru BRZ`, такой
  модели в каталоге нет) — откатывается на все модели этой марки, вместо
  пустого результата.
- `POST /api/leads/` — публично, без авторизации. Единая точка входа для
  всех обращений с сайта — `lead_type`: `complaint` (жалоба), `mat_order`
  (заказ коврика из конфигуратора), `product_order` (заказ товара).
  `multipart/form-data`: `name`, `phone` — всегда; `text` — обязателен при
  `complaint`; `car_model` — обязателен при `mat_order` (`material`/
  `mat_color`/`border_color`/`heel_color` — необязательные описательные
  пожелания, на цену не влияют; `logo` — необязательная наценка, см.
  ниже); `product_variant` — обязателен при `product_order`;
  `uploaded_photos` —
  необязательные файлы под одним ключом, для любого типа. Обязательность
  по типу проверяется в `LeadSerializer.validate()` (модель `Lead`,
  бывший `Complaint` — переименован и расширен в
  `lors/migrations/0016_rename_complaint_to_lead.py`). Ответ содержит
  `total_price` — рассчитанную итоговую цену (для `mat_order`: цена
  `car_model.price_category` + цена выбранного `logo`; для `product_order`:
  цена `product_variant`; `null`, если модель авто ещё не привязана к
  категории цены). Понятий «доплата за пакет» и «дэсе» как платных опций
  в бизнесе нет (проверено дважды с заказчиком) — соответствующие поля
  `Lead.has_package`/`Lead.dese` и модели `DeseOption`/`PricingSettings`
  убраны в `lors/migrations/0023_carmodel_cascade_fields_remove_package_dese.py`;
  «пакет» в каталоге — это `CarModel.package` (количество ковриков в
  комплекте, свойство конкретной модели, не доплата клиента), «дэсе» —
  `CarModel.driver_cut` (способ вырезки водительского коврика), см.
  `classify_price_categories.py` ниже.
- `GET /api/leads/` и `GET /api/leads/<id>/` — только для персонала
  (staff/`is_admin`), фильтры `?status=`/`?lead_type=`/`?car_model=`.
- `GET /api/settings/` — публично, без списка/id. Единая запись настроек
  сайта: адрес + координаты, «о компании», список `contacts` (телефоны,
  Instagram, Telegram, WhatsApp, Facebook, YouTube — сколько угодно штук
  каждого типа, с необязательной подписью). Редактируется только в `/admin/`
  (модель `SiteSettings` — синглтон, вторую запись создать нельзя;
  контакты — инлайном на той же странице, модель `Contact`).
- `POST /api/reviews/` — публично, без авторизации. `multipart/form-data`:
  `name`, `text`, `rating` (1–5, необязательно, по умолчанию 5), `photo`
  (одно фото, необязательно). `source` — только на чтение, публично
  созданные отзывы всегда `site`; `google` (для вручную перенесённых
  отзывов с Google) проставляется только в `/admin/`.
- `GET /api/reviews/` и `GET /api/reviews/<id>/` — тоже публично, но
  показывают только отзывы с `is_published=True` — публикация отзыва
  вручную через `/admin/` (модерация перед показом на сайте).
- `GET /api/pages/` и `GET /api/pages/<slug>/` — публично, только чтение.
  Контентные страницы (заголовок, текст, картинка), редактируются в
  `/admin/`. Заготовлены slug'и `about`/`franchise`/`production`/`materials`
  под будущий фронтенд (см. `lors/migrations/0012_seed_pages.py`), можно
  заводить и другие через админку.
- `GET /api/materials/` и `GET /api/colors/` — публично, только чтение,
  только активные (`is_active=True`) записи. `Material` (EVA
  локальный/импортный, ковролин 10/20мм) и `Color` — чисто описательные
  справочники для конфигуратора (клиент может указать пожелание), **на
  цену не влияют** — реальный прайс компании их не использует.
- `GET /api/price-categories/` — публично, только чтение. Реальные
  ценовые категории компании (`PriceCategory` — 12 категорий из
  прайс-листа: седан/джип/7 мест/бизнес/американец/минивэн, отдельно
  с пакетом и без, см. `lors/migrations/0020_seed_price_categories.py`).
  «С пакетом»/«без пакета» здесь — это про `CarModel.package`
  (комплектация конкретной модели, сколько ковриков в наборе), а не
  доплата, которую выбирает клиент — назначается через
  `classify_price_categories.py` (см. ниже), не вручную по каждой модели.
  `GET /api/car-models/<id>/` отдаёт `price_category` — категорию и
  готовую цену для этой модели (если не привязана — `null`).
- `GET /api/logo-options/` — публично, только чтение, только активные
  записи. Наценка из прайса: логотип (обычный 3$ / королевский 6$) —
  выбор клиента при заказе, суммируется с базовой ценой категории (см.
  `total_price` в `/api/leads/` выше).
- `GET /api/product-categories/` и `GET /api/products/` (фильтр
  `?category=<id>`) — публично, только чтение, только активные товары и
  варианты. Доп. товары (по образцу турецкой витрины сумок в багажник):
  `Product` — карточка товара, `ProductVariant` — конкретный размер/цвет/
  цена/фото (переиспользует `Color`). Ни каталог категорий, ни сами товары
  не заготовлены сидом — это реальные бизнес-данные, вносятся в `/admin/`.

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

### Разбор Марка→Модель→Кузов→Год из названия

`CarModel.name` — одна строка вида «Audi A4 II (B6, 8E) Седан
(2000 - 2006)», без отдельных полей под базовую модель/кузов/год. Чтобы
фронт мог показать пошаговый выбор Марка→Модель→Кузов→Год, не
перепроверяя вручную все 1087 моделей, `base_model`/`body_variant`/
`year_from`/`year_to` распознаются из `name` регуляркой:

```bash
python manage.py parse_car_models
```

Идемпотентна, безопасно перезапускать (после `import_catalog` или ручной
правки `name` через `/admin/`) — трогает только эти 4 поля, не
`car_type`/`price_category`/остальное, заполненное вручную. На текущем
каталоге распознаёт 1083/1087 (год почти всегда в последней скобочной
группе, но встречаются исключения — «Changan Alsvin 2018 - ...» без
скобок, «avatr 06(2026)» без диапазона, пара опечаток в годах).
Нераспознанные строки не трогает, логирует в
`data/model_parse_anomalies.log`.

Шаг «Кузов» на фронте комбинирует два независимых, слабо пересекающихся
источника: `car_type` (арабский, дозаполняется вручную в `/admin/`) и
`body_variant` (русское слово из названия, распознаётся этой командой) —
оба сейчас покрывают меньшинство каталога, показываются вместе одним
списком, с запасным пунктом на случай отсутствия обоих.

## Meta Conversions API

`lors/meta_capi.py` — серверная отправка события `Lead` в Meta (Facebook/
Instagram Ads) при создании заказа коврика или заказа товара через
`POST /api/leads/` (жалобы намеренно не отправляются — не тот сигнал, под
который стоит оптимизировать таргетинг рекламы). Дополняет браузерный Meta
Pixel — события не теряются из-за блокировщиков рекламы/ITP/третьих кук.

Персональные данные (телефон) уходят только в виде SHA-256-хэша от
нормализованного значения — так требует Meta, сырой номер не передаётся.
Email не собирается нигде в проекте (осознанно, чтобы не усложнять форму
заявки) — match rate у Meta будет ниже, чем при полном наборе полей, но
это ожидаемо.

Событие несёт не только факт заявки, а конкретный товар (`content_ids`/
`content_name`/`contents` — для коврика это модель авто, для товара —
вариант товара), чтобы Meta впоследствии могла использовать это для
динамического ретаргетинга. Полноценный каталог товаров в Meta Commerce
Manager (для показа объявлений с реальным товаром, не только сигнал
внутри события) — отдельная задача, в проекте пока не сделана.

Отправка — в отдельном потоке (не блокирует ответ `POST /api/leads/`),
сетевые ошибки только логируются и никогда не мешают созданию заявки.

Настройка через `.env`: `META_PIXEL_ID`, `META_ACCESS_TOKEN` (получаются в
Meta Events Manager → выбрать Pixel → Settings → Conversions API →
«Generate access token» — это делается в Meta Business Manager, не в этом
проекте). Пока оба пусты — интеграция тихо no-op'ится. `META_TEST_EVENT_CODE`
— опционально, для проверки в разделе «Test Events» Events Manager перед
боевым запуском.

## Ассистент — API + Telegram-бот с ИИ-поиском

Ответ клиенту генерируется целиком на бэкенде и отдаётся по HTTP — канал
(бот) сам ничего не генерирует, только пересылает сообщение и относит ответ
дальше:

- `POST /api/assistant/message/` — `{channel, external_user_id, text}` →
  `{reply}`. Закрыт заголовком `X-Assistant-Key` (должен совпадать с
  `ASSISTANT_API_KEY` из `.env`) — это внутренний сервисный вызов, не
  публичный эндпоинт сайта; без ключа доступ закрыт для всех
  (`assistant/permissions.py`, fail closed — в отличие от
  `TELEGRAM_BOT_TOKEN`/`ANTHROPIC_API_KEY`, где пустое значение просто
  выключает функцию, здесь пустое значение означает «никому нельзя»).
- `assistant/management/commands/runbot.py` — Telegram-бот (aiogram, long
  polling) — теперь тонкий HTTP-клиент этого эндпоинта (`httpx`), не прямой
  Python-вызов. Так же будет подключаться и любой будущий канал (Instagram,
  WhatsApp, веб-виджет) — своим адаптером поверх того же `/api/assistant/message/`,
  независимо от языка/процесса, в котором этот адаптер написан.

```bash
python manage.py runbot
```

Второй процесс рядом с `runserver` — при разработке через `run.sh` (см. ниже).
Нужны `TELEGRAM_BOT_TOKEN` (от [@BotFather](https://t.me/BotFather)),
`ASSISTANT_API_KEY` и `BACKEND_BASE_URL` (адрес, на котором поднят
Django — по умолчанию `http://127.0.0.1:8000`) в `.env`; `ANTHROPIC_API_KEY`
нужен самому бэкенду (для `/api/assistant/message/`), не боту.

Клиент пишет боту на любом языке (упор на сирийский диалект арабского) —
у Claude есть три инструмента (`assistant/claude_client.py`):

- `search_car_models` — дёргает тот же `smart_search_car_models`
  (`lors/search.py`), что и `/api/car-models/?search=`. Поиск идёт по
  всему каталогу, не только по марке/модели: код шаблона, тип авто, тип
  шофёра, пакет, примечания (`SEARCHABLE_FIELDS` в `lors/search.py`) —
  например, можно спросить прямо про код шаблона («есть код ب-11?»), и
  если ничего не нашлось, бот так и скажет, а не откажется искать.
  Результат уже включает базовую цену (`CarModel.price_category`), если
  она задана.
- `calculate_mat_price` — считает итоговую цену коврика с опцией логотипа
  той же формулой, что и `total_price` в `LeadSerializer`
  (`lors/serializers.py`) — цена категории + цена логотипа, если выбран.
- `search_products` — доп. товары (`Product`/`ProductVariant`, не
  коврики). Названия товаров/категорий в базе на арабском — инструмент
  ищет точную подстроку без перевода, поэтому в его описании прямо
  указано Claude самому переводить запрос клиента на арабский перед
  вызовом, если клиент написал на другом языке.

По найденной записи бот описывает, что есть для этой модели, и предлагает
контакты для заказа (`SiteSettings` — адрес, Instagram/Telegram/WhatsApp).

Бот помнит контекст переписки: перед каждым ответом `handle_message`
(`assistant/brain.py`) подтягивает последние `HISTORY_LIMIT` сообщений этого
пользователя из лога `BotMessage` и передаёт их в Claude как историю
диалога — так «2013 год» после «BMW X5» понимается как уточнение к прошлому
вопросу, а не новый пустой запрос.

Устройство:

- `assistant/views.py` — `AssistantMessageView`, HTTP-контракт
  (`POST /api/assistant/message/`), канал-агностичный
- `assistant/brain.py` — `handle_message(text, channel, external_user_id)`,
  вся логика ответа (история переписки + вызов Claude + лог), вызывается
  только из `AssistantMessageView`, напрямую больше нигде не импортируется
- `assistant/claude_client.py` — вызов Claude (`claude-opus-4-8`, ручной
  tool-use цикл, без beta tool_runner)
- `assistant/management/commands/runbot.py` — aiogram-адаптер, HTTP-клиент
  `/api/assistant/message/`; будущий Instagram/WhatsApp-адаптер будет
  дёргать тот же эндпоинт
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
