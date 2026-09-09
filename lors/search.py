import re

from django.db.models import Q

from .models import Brand, CarModel


SEARCHABLE_FIELDS = [
    'name', 'template_code', 'brand__name',
    'car_type', 'driver_cut', 'package', 'second_row_package', 'notes',
]

# Год в запросе часто не совпадает буквально с name ("2015" при диапазоне
# "2014 - 2018" в записи, или ассистент передаёт год слитно со скобками —
# "(2014-2018)" без пробелов, когда в name они есть) — раньше такое слово
# вообще ни с чем не совпадало, поиск откатывался на всю марку. Ищем год как
# ПОДСТРОКУ в любом токене (finditer, не полное совпадение слова), сверяем
# с year_from/year_to (parse_car_models) — в дополнение к прежней проверке
# на литеральную подстроку (OR, не замена — если поля не заполнены или год
# один в один совпадает текстом, старое поведение цело).
YEAR_IN_WORD_RE = re.compile(r'(?:19|20)\d{2}')


def smart_search_car_models(search: str):
    """Match every word of the query against every catalog field (model/brand
    name, template code, car type, driver cut, package, notes) — each word
    must appear *somewhere* in the record, not the whole query as one
    contiguous substring (so "BMW F10" matches "BMW 5 VI (F10) ..."). Falls
    back to the whole brand if nothing matches (e.g. a model the catalog
    doesn't have)."""
    qs = CarModel.objects.select_related('brand').all()
    words = search.split()
    query = Q()
    for word in words:
        word_query = Q()
        for field in SEARCHABLE_FIELDS:
            word_query |= Q(**{f'{field}__icontains': word})
        for year_match in YEAR_IN_WORD_RE.finditer(word):
            year = int(year_match.group())
            word_query |= Q(year_from__lte=year, year_to__gte=year)
            word_query |= Q(year_from=year, year_to__isnull=True)
        query &= word_query
    exact = qs.filter(query) if words else qs.none()
    if exact.exists():
        return exact

    brand = match_brand(search)
    if brand:
        return qs.filter(brand=brand)
    return qs.none()


def match_brand(search: str):
    words = search.split()
    for word_count in range(len(words), 0, -1):
        candidate = ' '.join(words[:word_count])
        brand = Brand.objects.filter(name__icontains=candidate).first()
        if brand:
            return brand
    return None
