"""
Общая часть ассистента, не зависящая от провайдера (Claude/OpenAI/DeepSeek —
см. claude_client.py/openai_client.py/deepseek_client.py): системный промпт
и три инструмента (function calling). Все три провайдера используют один и
тот же TOOL_DEFS и TOOL_HANDLERS — отличаются только тем, как заворачивают
эти же данные в свой собственный формат tool-use (Anthropic input_schema /
OpenAI Responses parameters / DeepSeek-Chat-Completions — по форме это один
и тот же JSON Schema, разнится только оборачивающий ключ).
"""

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
                        "сообщения клиента."
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
                    'description': 'Название варианта логотипа из системного промпта, например "Обычный".',
                },
                'dese': {
                    'type': 'string',
                    'description': 'Название варианта дэсе из системного промпта, например "Тип 1".',
                },
            },
            'required': ['car_model_query'],
        },
    },
]


def _format_contacts(contacts) -> str:
    type_names = dict(Contact.TYPE_CHOICES)
    by_type = {}
    for c in contacts:
        value = f'{c.value} ({c.label})' if c.label else c.value
        by_type.setdefault(c.contact_type, []).append(value)
    if not by_type:
        return '—'
    return '; '.join(f'{type_names[t]}: ' + ', '.join(vals) for t, vals in by_type.items())


def _format_pricing_options() -> str:
    package_price = PricingSettings.load().package_price
    logos = ', '.join(f'{o.name} (+{o.price}$)' for o in LogoOption.objects.filter(is_active=True))
    deses = ', '.join(f'{o.name} (+{o.price}$)' for o in DeseOption.objects.filter(is_active=True))
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
        'используя контакты ниже. Не повторяй контакты в каждом сообщении подряд — только '
        'когда это уместно. '
        'Если вопрос клиента не про каталог и не про товары — отвечай как обычный дружелюбный '
        'ассистент компании, инструмент не вызывай.\n\n'
        f'Контакты: адрес {s.address or "—"}. {contacts_line}.'
    )


def _run_search_tool(query: str) -> str:
    results = list(smart_search_car_models(query).select_related('price_category')[:10])
    if not results:
        return 'Ничего не найдено.'
    return '\n'.join(
        f'{m.brand.name} {m.name} | код шаблона: {m.template_code or "—"} | '
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
        names = ', '.join(f'{m.brand.name} {m.name}' for m in results[:5])
        return f'Найдено несколько моделей, уточни у клиента какая именно: {names}'

    cm = results[0]
    if not cm.price_category:
        return f'Для {cm.brand.name} {cm.name} цена ещё не задана — нужно уточнить у менеджера.'

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
