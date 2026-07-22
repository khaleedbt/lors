import anthropic
from django.conf import settings

from lors.models import SiteSettings
from lors.search import smart_search_car_models

MODEL = 'claude-opus-4-8'
MAX_TOOL_ROUNDS = 3

SEARCH_TOOL = {
    'name': 'search_car_models',
    'description': (
        'Найти записи в каталоге LORS по любому полю: марка, модель, код шаблона, '
        'тип автомобиля, тип шофёра/дасэ, пакет, примечания. Используй для ЛЮБОГО '
        'вопроса про каталог, не только про марку/модель.'
    ),
    'input_schema': {
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
}


def _client():
    if settings.ANTHROPIC_API_KEY:
        return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return anthropic.Anthropic()  # falls back to the SDK's own credential resolution


def _system_prompt() -> str:
    s = SiteSettings.load()
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
        '(тоже не всё сразу, а спроси, интересно ли).\n'
        'В конце, когда вариант определён и клиент готов к заказу, предложи связаться, '
        'используя контакты ниже. Не повторяй контакты в каждом сообщении подряд — только '
        'когда это уместно. '
        'Если вопрос клиента не про каталог — отвечай как обычный дружелюбный ассистент компании, '
        'инструмент не вызывай.\n\n'
        f'Контакты: адрес {s.address or "—"}, Instagram {s.instagram_url or "—"}, '
        f'Telegram {s.telegram_url or "—"}, WhatsApp {s.whatsapp_url or "—"}.'
    )


def _run_search_tool(query: str) -> str:
    results = list(smart_search_car_models(query)[:10])
    if not results:
        return 'Ничего не найдено.'
    return '\n'.join(
        f'{m.brand.name} {m.name} | код шаблона: {m.template_code or "—"} | '
        f'тип авто: {m.car_type or "—"} | шофёр: {m.driver_cut or "—"} | '
        f'пакет: {m.package or "—"} | 2-й ряд: {m.second_row_package or "—"} | '
        f'примечания: {m.notes or "—"}'
        for m in results
    )


def ask_claude(user_text: str, history: list[dict] | None = None) -> str:
    client = _client()
    messages = (history or []) + [{'role': 'user', 'content': user_text}]

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=_system_prompt(),
            tools=[SEARCH_TOOL],
            messages=messages,
        )

        if response.stop_reason != 'tool_use':
            return next((b.text for b in response.content if b.type == 'text'), '')

        messages.append({'role': 'assistant', 'content': response.content})
        tool_results = [
            {
                'type': 'tool_result',
                'tool_use_id': block.id,
                'content': _run_search_tool(block.input['query']),
            }
            for block in response.content if block.type == 'tool_use'
        ]
        messages.append({'role': 'user', 'content': tool_results})

    return 'Извини, не получилось обработать запрос — напиши нам напрямую.'
