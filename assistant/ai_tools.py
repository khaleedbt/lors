"""
Общая часть ассистента, не зависящая от провайдера (Claude/OpenAI/DeepSeek —
см. claude_client.py/openai_client.py/deepseek_client.py): системный промпт
и три инструмента (function calling). Все три провайдера используют один и
тот же TOOL_DEFS и TOOL_HANDLERS — отличаются только тем, как заворачивают
эти же данные в свой собственный формат tool-use (Anthropic input_schema /
OpenAI Responses parameters / DeepSeek-Chat-Completions — по форме это один
и тот же JSON Schema, разнится только оборачивающий ключ).
"""

import re

from django.db.models import Q

from lors.models import Contact, DeseOption, LogoOption, Product, PricingSettings, SiteSettings
from lors.search import smart_search_car_models

TOOL_DEFS = [
    {
        'name': 'search_car_models',
        'description': (
            'Найти записи в каталоге LORS по любому полю: марка, модель, код шаблона, '
            'тип автомобиля, тип шофёра/дасэ, пакет, примечания. Используй для ЛЮБОГО '
            'вопроса про каталог, не только про марку/модель. Результат уже содержит '
            'базовую цену коврика для найденной модели (если она задана).'
        ),
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': (
                        "Ключевое слово или фраза для поиска — марка ('BMW'), модель "
                        "('Subaru XV'), код шаблона ('ب-38', 'أ-12') или другой признак "
                        "из каталога. Передавай только сам термин, без лишних слов из "
                        "сообщения клиента. ВАЖНО: марки и модели в каталоге записаны "
                        "латиницей (BMW, Toyota Camry), даже если клиент написал их "
                        "по-арабски или кириллицей — ищи латинской транслитерацией "
                        "('كامري' -> 'Camry'), а не оригинальным написанием клиента."
                    ),
                },
            },
            'required': ['query'],
        },
    },
    {
        'name': 'search_products',
        'description': (
            'Найти дополнительные товары компании — не коврики, а сумки в багажник, '
            'органайзеры и т.п. По названию товара или категории. У каждого товара '
            'несколько вариантов (размер/цвет), у каждого варианта своя цена. '
            'ВАЖНО: названия товаров и категорий в базе — на арабском, поиск ищет '
            'точное вхождение подстроки без перевода. Если клиент спросил не по-арабски '
            '(например по-русски "органайзер" или по-английски "organizer") — сначала '
            'сам переведи ключевое слово на арабский и ищи именно им, а не оригинальным '
            'словом клиента.'
        ),
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': (
                        "Ключевое слово на арабском (переведи, если клиент писал на другом "
                        "языке) — название товара или категории, например 'منظم' или 'حقيبة'."
                    ),
                },
            },
            'required': ['query'],
        },
    },
    {
        'name': 'calculate_mat_price',
        'description': (
            'Посчитать итоговую цену коврика для конкретной модели авто с учётом '
            'опций: коврик в багажник, логотип, дэсе (подпятник). Модель для расчёта '
            'сначала нужно найти через search_car_models — сюда передавай точное '
            'название модели из его результатов (или марку+модель), не произвольный '
            'текст клиента. Опции передавай, только если клиент их упомянул — '
            'без них посчитается база стоимость по категории.'
        ),
        'parameters': {
            'type': 'object',
            'properties': {
                'car_model_query': {
                    'type': 'string',
                    'description': 'Точное название модели (как в результатах search_car_models), не свободный текст.',
                },
                'has_package': {
                    'type': 'boolean',
                    'description': (
                        'Клиент хочет добавить коврик в багажник за отдельную плату (только если у '
                        'модели багажника ещё нет в базовой категории). НЕ путать с "пакетом опций" '
                        'в общем смысле — это конкретно коврик в багажник.'
                    ),
                },
                'logo': {
                    'type': 'string',
                    'description': (
                        'Название варианта логотипа — СКОПИРУЙ буквально, символ в символ, из списка '
                        '"Варианты логотипа" в системном промпте (он на арабском и может поменяться '
                        'в любой момент). НЕ переводи, не транслитерируй и не придумывай название сам.'
                    ),
                },
                'dese': {
                    'type': 'string',
                    'description': (
                        'Название варианта дэсе — СКОПИРУЙ буквально, символ в символ, из списка '
                        '"Варианты дэсе" в системном промпте (он на арабском и может поменяться '
                        'в любой момент). НЕ переводи, не транслитерируй и не придумывай название сам.'
                    ),
                },
            },
            'required': ['car_model_query'],
        },
    },
]


def _whatsapp_url(phone: str) -> str:
    """wa.me принимает номер только цифрами, без +/пробелов/скобок."""
    digits = re.sub(r'\D', '', phone)
    return f'https://wa.me/{digits}'


def _format_contacts(contacts) -> str:
    # Для телефона/WhatsApp собираем готовую markdown-ссылку [текст](url) —
    # бот (runbot.py, markdown_to_telegram_html) превращает её в кликабельную
    # ссылку на WhatsApp. Ссылку собираем сами, а не поручаем это ИИ: он тот
    # же номер может передать с ошибкой в цифрах или формате wa.me (тот же
    # класс риска, что и с logo/dese — см. calculate_mat_price выше).
    type_names = dict(Contact.TYPE_CHOICES)
    by_type = {}
    for c in contacts:
        value = c.value
        if c.contact_type in (Contact.TYPE_PHONE, Contact.TYPE_WHATSAPP):
            value = f'[{c.value}]({_whatsapp_url(c.value)})'
        if c.label:
            value = f'{value} ({c.label})'
        by_type.setdefault(c.contact_type, []).append(value)
    if not by_type:
        return '—'
    return '; '.join(f'{type_names[t]}: ' + ', '.join(vals) for t, vals in by_type.items())


def _format_pricing_options() -> str:
    # LogoOption с 0029_moysklad_colors_and_brand_logos пошла по маркам —
    # один и тот же "Обычный"/"Malaki" физически разный шильдик на каждую
    # марку (~40 строк на одно название), но ЦЕНА одна и та же. В промпт
    # нужны только различающиеся (название, цена) пары, а не все 80+ строк
    # — иначе список раздувается копипастой одного и того же на каждую
    # марку (см. историю бага в этом коммите).
    # .order_by() сбрасывает Meta.ordering модели (order, id) — иначе Postgres
    # тянет их в ORDER BY поверх DISTINCT, и одинаковые (name, price) не
    # схлопываются, т.к. id всё равно у каждой строки уникален.
    package_price = PricingSettings.load().package_price
    logo_prices = LogoOption.objects.filter(is_active=True).order_by().values_list('name', 'price').distinct()
    dese_prices = DeseOption.objects.filter(is_active=True).order_by().values_list('name', 'price').distinct()
    logos = ', '.join(f'{name} (+{price}$)' for name, price in logo_prices)
    deses = ', '.join(f'{name} (+{price}$)' for name, price in dese_prices)
    return (
        f'Добавить коврик в багажник (если у модели его ещё нет в базовой категории): +{package_price}$. '
        f'Варианты логотипа: {logos or "—"}. Варианты дэсе (подпятника): {deses or "—"}.'
    )


def system_prompt() -> str:
    s = SiteSettings.load()
    contacts_line = _format_contacts(s.contacts.all())
    return (
        'Ты — ассистент-консультант LORS SYRIA, компании по пошиву автоковриков по лекалам. '
        'Отвечай на языке клиента; если клиент пишет по-арабски — используй сирийский диалект.\n\n'
        'СТИЛЬ ОБЩЕНИЯ — как живой консультант, у которого есть база под рукой, '
        'а не как выгрузка из этой базы:\n'
        '- Отвечай кратко и по существу — 2-4 предложения на большинство ответов, без '
        'лишних вводных фраз и повторов уже сказанного. Не используй эмодзи/смайлики '
        'ни при каких обстоятельствах, ни на каком языке.\n'
        '- Веди диалог поэтапно, один уточняющий вопрос за раз. Не вываливай в одном '
        'сообщении сразу все поколения/варианты модели таблицей или списком — это '
        'перегружает клиента.\n'
        '- Если по запросу нашлось НЕСКОЛЬКО вариантов (разные поколения, годы, кузова) — '
        'не показывай их все сразу. Кратко скажи, что для этой модели есть несколько '
        'поколений/вариантов, и спроси уточнение (год выпуска, кузов, что важнее для клиента), '
        'чтобы сузить до одного.\n'
        '- Как только вариант остался один — подтверди обычными словами, что коврик под эту '
        'модель есть, и своими словами опиши, что за комплектация/тип/особенности (не как список '
        'технических полей "тип: X | пакет: Y", а естественным предложением, как будто ты это '
        'просто знаешь). НИКОГДА не называй и не упоминай клиенту внутренний код шаблона '
        '(например ب-11, 2-ب) — это служебная информация для сотрудников, клиенту она не нужна '
        'и не должна фигурировать в переписке ни в каком виде.\n'
        '- Результаты поиска у тебя уже есть в контексте после вызова инструмента — для '
        'уточняющего ответа НЕ нужно вызывать инструмент заново, если условие клиента можно '
        'сопоставить с уже полученными данными.\n\n'
        'У тебя есть инструмент search_car_models — вызывай его для ЛЮБОГО вопроса про каталог: '
        'марка, модель, код шаблона, тип авто, тип шофёра/дасэ, пакет, примечания. '
        'Не отказывай в поиске по коду или другому признаку — просто вызови инструмент с этим значением. '
        'Если клиент упомянул что-то из каталога внутри длинной фразы — вычлени именно термин '
        '(код, марку, модель) и ищи по нему, а не по всей фразе целиком.\n'
        'Если по коду/запросу ничего не нашлось — так и скажи, не выдумывай. '
        'Если искали конкретную модель и её нет, но есть другие модели этой марки — предложи их '
        '(тоже не всё сразу, а спроси, интересно ли).\n\n'
        'ЦЕНА КОВРИКА: search_car_models уже возвращает базовую цену найденной модели (если задана). '
        'Озвучивай её обычными словами ("выйдет в 120 долларов"), не как техническое поле. '
        'Если клиент спрашивает про доп. опции (коврик в багажник/логотип/дэсе) или хочет точную '
        'цену с ними — '
        'сначала уточни, какие именно опции нужны (по одной за раз, не все сразу), затем вызови '
        'calculate_mat_price с этими опциями и озвучь итоговую сумму из его ответа. '
        'Если у модели ещё нет заданной цены (search_car_models не показал цену) — так и скажи, '
        'уточнить может только менеджер, не выдумывай сумму.\n\n'
        'ТОВАРЫ: если клиент спрашивает про что-то, кроме коврика (сумки, органайзеры и т.п.) — '
        'используй search_products, не search_car_models.\n\n'
        f'{_format_pricing_options()}\n\n'
        'В конце, когда вариант определён и клиент готов к заказу, предложи связаться, '
        'используя контакты ниже. Телефон/WhatsApp там уже даны в виде markdown-ссылки '
        '[номер](https://wa.me/...) — приведи её В ТОЧНОСТИ как есть, не убирай квадратные '
        'скобки и не переписывай номер отдельным текстом, иначе ссылка станет некликабельной. '
        'Не повторяй контакты в каждом сообщении подряд — только когда это уместно. '
        'Если вопрос клиента не про каталог и не про товары — отвечай как обычный дружелюбный '
        'ассистент компании, инструмент не вызывай.\n\n'
        f'Контакты: адрес {s.address or "—"}. {contacts_line}.'
    )


def _car_display_name(m) -> str:
    """base_model/body_variant — уже очищены и переведены на арабский
    (parse_car_models), в отличие от сырого m.name, где ещё остаются
    служебные русские слова вроде "Рестайлинг"/"Дорестайлинг". Отдавать
    ИИ именно это, а не name — гарантия, что такие слова не долетят до
    клиента, не зависящая от того, послушается ли модель текстовой
    инструкции. Падаем на m.name только для ~4 строк каталога, где
    base_model не распознан (см. data/model_parse_anomalies.log)."""
    if not m.base_model:
        return f'{m.brand.name} {m.name}'
    year_range = ''
    if m.year_from and m.year_to and m.year_from != m.year_to:
        year_range = f'{m.year_from}-{m.year_to}'
    elif m.year_from:
        year_range = str(m.year_from)
    extras = ', '.join(filter(None, [m.body_variant, year_range]))
    return f'{m.brand.name} {m.base_model} ({extras})' if extras else f'{m.brand.name} {m.base_model}'


def _run_search_tool(query: str) -> str:
    results = list(smart_search_car_models(query).select_related('price_category')[:10])
    if not results:
        return 'Ничего не найдено.'
    return '\n'.join(
        f'{_car_display_name(m)} | код шаблона: {m.template_code or "—"} | '
        f'тип авто: {m.car_type or "—"} | шофёр: {m.driver_cut or "—"} | '
        f'пакет: {m.package or "—"} | 2-й ряд: {m.second_row_package or "—"} | '
        f'примечания: {m.notes or "—"} | '
        f'цена: {f"{m.price_category.price}$ ({m.price_category.name})" if m.price_category else "не задана"}'
        for m in results
    )


def _run_product_search_tool(query: str) -> str:
    products = Product.objects.filter(is_active=True).filter(
        Q(name__icontains=query) | Q(category__name__icontains=query),
    ).select_related('category').prefetch_related('variants__color')[:10]
    if not products:
        return 'Товары не найдены.'
    lines = []
    for p in products:
        variants = [v for v in p.variants.all() if v.is_active]
        variant_text = '; '.join(
            f'{v.size or "—"}{" " + v.color.name if v.color else ""}: {v.price}$' for v in variants
        )
        category = p.category.name if p.category else 'без категории'
        lines.append(f'{p.name} ({category}): {variant_text or "нет доступных вариантов"}')
    return '\n'.join(lines)


def _run_calculate_tool(car_model_query: str, has_package: bool = False, logo: str | None = None, dese: str | None = None) -> str:
    results = list(smart_search_car_models(car_model_query).select_related('price_category')[:5])
    if not results:
        return 'Модель не найдена — сначала используй search_car_models, чтобы получить точное название.'
    if len(results) > 1:
        names = ', '.join(_car_display_name(m) for m in results[:5])
        return f'Найдено несколько моделей, уточни у клиента какая именно: {names}'

    cm = results[0]
    if not cm.price_category:
        return f'Для {_car_display_name(cm)} цена ещё не задана — нужно уточнить у менеджера.'

    total = cm.price_category.price
    breakdown = [f'{cm.price_category.name}: {cm.price_category.price}$']

    if has_package:
        package_price = PricingSettings.load().package_price
        total += package_price
        breakdown.append(f'коврик в багажник: +{package_price}$')

    if logo:
        logo_obj = LogoOption.objects.filter(name__iexact=logo, is_active=True).first()
        if logo_obj:
            total += logo_obj.price
            breakdown.append(f'логотип «{logo_obj.name}»: +{logo_obj.price}$')
        else:
            breakdown.append(f'(логотип "{logo}" не найден в списке вариантов — не учтён)')

    if dese:
        dese_obj = DeseOption.objects.filter(name__iexact=dese, is_active=True).first()
        if dese_obj:
            total += dese_obj.price
            breakdown.append(f'дэсе «{dese_obj.name}»: +{dese_obj.price}$')
        else:
            breakdown.append(f'(дэсе "{dese}" не найден в списке вариантов — не учтён)')

    return '; '.join(breakdown) + f' | Итого: {total}$'


TOOL_HANDLERS = {
    'search_car_models': lambda i: _run_search_tool(i['query']),
    'search_products': lambda i: _run_product_search_tool(i['query']),
    'calculate_mat_price': lambda i: _run_calculate_tool(
        i['car_model_query'], i.get('has_package', False), i.get('logo'), i.get('dese'),
    ),
}
