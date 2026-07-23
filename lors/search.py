from django.db.models import Q

from .models import Brand, CarModel


SEARCHABLE_FIELDS = [
    'name', 'template_code', 'brand__name',
    'car_type', 'driver_cut', 'package', 'second_row_package', 'notes',
]


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
