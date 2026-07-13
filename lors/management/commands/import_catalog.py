"""
Import the catalog from data/Лист1.csv (produced by scripts/fetch_sheet.py)
into the Brand / CarModel tables.

Sheet layout: column 0 holds either a bare brand name ("Audi", "Haval", ...)
or a full model name ("Audi A3 I (8L) (1996 - 2000)"). Only a minority of
model rows have columns 1-7 filled in (template code, car type, etc.) —
most are catalog entries still waiting on a template. So brand vs. model
can't be told apart by "has other columns filled"; instead a row counts as
a model if its name looks like one (contains a parenthesis or a 4-digit
year):
    0 name | 1 template_code | 2 car_type | 3 driver_cut
    4 package | 5 second_row_package | 6 notes | 7 video_url
Columns 8+ carry no real data in the current sheet and are ignored.

A name that doesn't look like a model is normally a brand header — but the
sheet also has typos that produce the same shape (a model name missing its
parenthesis/year, e.g. "mercedes-BenzCitan" instead of "Mercedes-Benz Citan
(...)"). Treating those as new brands would silently reattribute every
model below them until the next real brand header. So such a row is only
promoted to a brand if it doesn't extend the current brand's name and isn't
obviously garbage (digit-only, or a handful of repeated characters);
otherwise it's logged as an anomaly and the current brand stays unchanged.

The source has duplicate model names (sometimes with different template
codes, sometimes blank repeats of an already-filled row) — collapsing on
(brand, name) would silently overwrite good data with blanks. Each sheet
row is instead kept as its own CarModel, identified by sheet_row, so
duplicates are preserved and reruns stay idempotent.

Rows that don't fit this shape (missing name, oversized junk cell, a
"model-shaped" row with fields but a name that doesn't look like a model)
are skipped and logged rather than guessed at.

car_type/package are strict single-choice fields (see CarModel.CAR_TYPE_CHOICES /
PACKAGE_CHOICES); rows with several comma-separated values in those cells keep
just the first and log the rest instead of being skipped.
"""

import pathlib
import re

import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from lors.models import Brand, CarModel

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent / 'data'
DEFAULT_CSV = DATA_DIR / 'Лист1.csv'

FIELD_COLUMNS = {
    'template_code': 1,
    'car_type': 2,
    'driver_cut': 3,
    'package': 4,
    'second_row_package': 5,
    'notes': 6,
    'video_url': 7,
}
MAX_NAME_LENGTH = 500
MAX_BRAND_NAME_LENGTH = 40
WELL_FORMED_NAME = re.compile(r'\(|\d{4}')  # has a parenthesis or a 4-digit year

# car_type/package are strict single-choice dropdowns (see CarModel.CAR_TYPE_CHOICES /
# PACKAGE_CHOICES) but the sheet sometimes crams several comma-separated values into one
# cell — keep just the first so the value matches the choices.
COMBO_FIELDS = ['car_type', 'package']


def normalize(text):
    return re.sub(r'[\s\-]', '', text).lower()


def looks_like_junk_brand_name(name):
    if name.isdigit():
        return True
    unique_chars = set(name.replace(' ', ''))
    return len(unique_chars) <= 2 and len(name) > 3


def extends_current_brand(name, current_brand):
    if current_brand is None:
        return False
    normalized_name = normalize(name)
    normalized_brand = normalize(current_brand.name)
    return normalized_name != normalized_brand and normalized_name.startswith(normalized_brand)


class Command(BaseCommand):
    help = 'Import Brand/CarModel rows from data/Лист1.csv'

    def add_arguments(self, parser):
        parser.add_argument('--file', default=str(DEFAULT_CSV), help='path to the sheet CSV')

    def handle(self, *args, **options):
        csv_path = pathlib.Path(options['file'])
        if not csv_path.exists():
            raise CommandError(f'{csv_path} not found — run scripts/fetch_sheet.py first')

        df = pd.read_csv(csv_path, header=None, dtype=str).fillna('')

        current_brand = None
        created, updated = 0, 0
        anomalies = []

        for row_idx, row in df.iterrows():
            name = row[0].strip()
            fields = {key: row[col].strip() for key, col in FIELD_COLUMNS.items()}
            has_fields = any(fields.values())

            for field in COMBO_FIELDS:
                if ',' in fields[field]:
                    original = fields[field]
                    fields[field] = original.split(',')[0].strip()
                    anomalies.append(f'row {row_idx}: {field} had combined values {original!r}, kept {fields[field]!r}')

            if not name and not has_fields:
                continue

            if len(name) > MAX_NAME_LENGTH:
                anomalies.append(f'row {row_idx}: oversized name cell ({len(name)} chars), skipped')
                continue

            if not name:
                anomalies.append(f"row {row_idx}: model data without a name (template_code={fields['template_code']!r}), skipped")
                continue

            looks_like_model = bool(WELL_FORMED_NAME.search(name))

            if not looks_like_model:
                if has_fields:
                    anomalies.append(f"row {row_idx}: unrecognized name format {name!r}, has fields but doesn't look like a model, skipped")
                elif len(name) > MAX_BRAND_NAME_LENGTH or looks_like_junk_brand_name(name) or extends_current_brand(name, current_brand):
                    anomalies.append(f"row {row_idx}: unrecognized name format {name!r}, not promoted to a brand, skipped")
                else:
                    current_brand, _ = Brand.objects.get_or_create(name=name)
                continue

            if current_brand is None:
                anomalies.append(f'row {row_idx}: model row before any brand header ({name!r}), skipped')
                continue

            _, was_created = CarModel.objects.update_or_create(
                sheet_row=row_idx,
                defaults={**fields, 'brand': current_brand, 'name': name},
            )
            created += was_created
            updated += not was_created

        self.stdout.write(self.style.SUCCESS(
            f'brands: {Brand.objects.count()}, car models created: {created}, updated: {updated}'
        ))

        if anomalies:
            self.stdout.write(self.style.WARNING(f'{len(anomalies)} rows need attention (skipped or auto-fixed):'))
            for line in anomalies:
                self.stdout.write(f'  - {line}')

            log_path = DATA_DIR / 'import_anomalies.log'
            log_path.write_text('\n'.join(anomalies) + '\n', encoding='utf-8')
            self.stdout.write(self.style.WARNING(f'anomaly log written to {log_path}'))
