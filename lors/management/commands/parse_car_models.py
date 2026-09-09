"""
Derive CarModel.base_model / body_variant / year_from / year_to from the
free-text `name` field, so the frontend can offer a Марка→Модель→Кузов→Год
cascade without a manual re-tagging pass over the whole catalog.

`name` was never structured — it's whatever the source sheet's row label
was, e.g. "Audi A4 II (B6, 8E) Седан (2000 - 2006)" or, just as often,
"Changan Alsvin 2018 - ..." (no parens at all) or "avatr 06(2026)" (single
year, no range). This command is a best-effort regex parse, not a strict
grammar: real close year-range parens far outnumber the exceptions in the
current catalog (95/1087 lack a recognizable year at all), but exceptions
exist. Rows where no year can be found at all are left untouched and
logged to data/model_parse_anomalies.log for manual review, rather than
guessing.

Idempotent and safe to re-run any time (after import_catalog adds new
rows, or after someone edits a name by hand) — it only ever overwrites
base_model/body_variant/year_from/year_to, computed fresh from `name`
every time; it never touches car_type, price_category or anything a human
filled in through the admin.

body_variant is stored in Arabic (BODY_VARIANT_MAP), not the Cyrillic word
matched in `name` — this is client-facing (site cascade selector, assistant
tool results), and the site is Arabic-only. "Рестайлинг"/"Дорестайлинг" are
stripped from base_model and not stored anywhere — they're never shown to a
client, so no translation needed there. "Long"/"Sportback" are deliberately
left inside base_model as-is (not recognized body-variant words) — not
translating those was a conscious call, not an oversight.
"""

import pathlib
import re

from django.core.management.base import BaseCommand

from lors.models import CarModel

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent / 'data'

# Ключ — то, что реально встречается в исходном name (кириллица, из
# исходной таблицы); значение — что сохраняется в body_variant и в итоге
# уходит клиенту (сайт/бот — только на арабском, см. обсуждение перевода).
BODY_VARIANT_MAP = {
    'Седан': 'سيدان',
    'Хэтчбек': 'هاتشباك',
    'Универсал': 'ستيشن واغن',
    'Купе': 'كوبيه',
    'Кроссовер': 'كروس أوفر',
    'Внедорожник': 'دفع رباعي',
    'Лифтбек': 'ليفت باك',
    'Минивэн': 'ميني فان',
    'Пикап': 'بيك أب',
    'Родстер': 'رودستر',
    'Кабриолет': 'مكشوفة',
    'Фастбек': 'فاست باك',
}
BODY_VARIANT_RE = re.compile('|'.join(BODY_VARIANT_MAP))

# "(2000 - 2006)", "(2000-2006)", "(2000 – 2006)", "(2018-...)", "2018 - ..." (no parens),
# "(2026)" (single year, no dash) — always a 19xx/20xx year, optionally followed by a
# dash and a second (19xx/20xx) year; anything after a dash that isn't a clean second
# year (truncated "202..", "н.в.", missing) is treated as open-ended.
YEAR_RANGE_RE = re.compile(
    r'(?P<from>(?:19|20)\d{2})\s*[-–]\s*(?P<to>(?:19|20)\d{2})?[.\s]*(?=\)|$|[^\d])'
)
YEAR_ONLY_RE = re.compile(r'(?:19|20)\d{2}')

PAREN_RE = re.compile(r'\([^()]*\)')
RESTYLE_RE = re.compile(r'\b(Рестайлинг|Дорестайлинг)\s*\d*\b', re.IGNORECASE)
TRAILING_ROMAN_RE = re.compile(r'\s+[IVXLCDM]+$')
WHITESPACE_RE = re.compile(r'\s+')


def parse_years(name):
    """Return (year_from, year_to, matched_span) of the last recognizable
    year (range) in the string, or (None, None, None) if none found."""
    last = None
    for m in YEAR_RANGE_RE.finditer(name):
        last = m
    if last:
        year_from = int(last.group('from'))
        year_to = int(last.group('to')) if last.group('to') else None
        return year_from, year_to, last.span()

    last_year = None
    for m in YEAR_ONLY_RE.finditer(name):
        last_year = m
    if last_year:
        year = int(last_year.group())
        return year, year, last_year.span()

    return None, None, None


def parse_body_variant(name):
    """Возвращает (исходное_слово_из_name, арабский_перевод) — исходное
    нужно, чтобы вырезать его из name при сборке base_model (там ещё
    кириллица), а перевод — то, что реально сохраняется в body_variant
    и в итоге видит клиент (сайт/бот — только на арабском)."""
    m = BODY_VARIANT_RE.search(name)
    if not m:
        return '', ''
    matched = m.group(0)
    return matched, BODY_VARIANT_MAP[matched]


def derive_base_model(name, year_span, matched_ru_word):
    text = name[:year_span[0]] + name[year_span[1]:]
    text = PAREN_RE.sub(' ', text)
    if matched_ru_word:
        text = text.replace(matched_ru_word, ' ')
    text = RESTYLE_RE.sub(' ', text)
    text = WHITESPACE_RE.sub(' ', text).strip(' -–,')
    # Strip a trailing roman-numeral generation marker ("Audi A3 I/II/III..." ->
    # "Audi A3") so different generations of the same model group together —
    # only reachable once trailing whitespace from the removals above is
    # already collapsed, otherwise "I   " never matches an end-of-string anchor.
    text = TRAILING_ROMAN_RE.sub('', text).strip()
    return text


class Command(BaseCommand):
    help = 'Re-derive CarModel.base_model/body_variant/year_from/year_to from name (idempotent)'

    def handle(self, *args, **options):
        updated = 0
        anomalies = []

        for car_model in CarModel.objects.all():
            year_from, year_to, year_span = parse_years(car_model.name)
            if year_span is None:
                anomalies.append(f'id {car_model.id}: no recognizable year in {car_model.name!r}, left untouched')
                continue

            matched_ru_word, body_variant = parse_body_variant(car_model.name)
            base_model = derive_base_model(car_model.name, year_span, matched_ru_word)
            if not base_model:
                anomalies.append(
                    f'id {car_model.id}: year parsed ({year_from}-{year_to}) but base_model came out empty '
                    f'for {car_model.name!r}, left untouched'
                )
                continue

            car_model.base_model = base_model
            car_model.body_variant = body_variant
            car_model.year_from = year_from
            car_model.year_to = year_to
            car_model.save(update_fields=['base_model', 'body_variant', 'year_from', 'year_to'])
            updated += 1

        total = CarModel.objects.count()
        self.stdout.write(self.style.SUCCESS(f'updated {updated}/{total} car models'))

        if anomalies:
            self.stdout.write(self.style.WARNING(f'{len(anomalies)} rows need attention (left untouched):'))
            for line in anomalies:
                self.stdout.write(f'  - {line}')

            log_path = DATA_DIR / 'model_parse_anomalies.log'
            log_path.write_text('\n'.join(anomalies) + '\n', encoding='utf-8')
            self.stdout.write(self.style.WARNING(f'anomaly log written to {log_path}'))
