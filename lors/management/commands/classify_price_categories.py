"""
Разносит CarModel по ценовым категориям (PriceCategory) — Этап 5 из плана
внедрения реального прайс-листа компании.

Как это устроено: сегмент (седан/джип/7 мест/7 мест бизнес/американец/
Land Cruiser/минивэн Carnival-Staria-H1) определяется по знаниям об
автомобилях — марка/модель однозначно говорят, какой это тип кузова и
сколько мест. Это сделал я (Claude), а не бизнес-правило из каталога.

А вот тариф «с пакетом» / «без пакета» определить по машине нельзя — это
решение о конкретной комплектации, которую производит компания для этой
записи каталога, а не о свойстве автомобиля. Здесь используется то, что
уже есть в данных: если у CarModel.package стоит "لا يوجد باكاج" (нет
пакета) — берём тариф «без пакета», иначе (пусто или указано число
деталей) — «с пакетом» (это дефолт, подтверждённый бизнесом: полная цена
безопаснее для маржи, чем случайно продешевить).

Пикапы и коммерческие грузовики/фургоны (Ford Ranger/F-150, Toyota Hilux,
Dodge RAM, Mercedes Sprinter/Actros и т.п.) в прайс-листе вообще
отсутствуют как категория — для них price_category сознательно
оставляется пустым (это законный "требует уточнения бизнесом", а не баг).

Категория "7 мест бизнес" против обычной "7 мест": если в названии прямо
есть "رجال أعمال"/"business" — бизнес; иначе — по бренду (Land Rover,
Lexus, Infiniti, Genesis, Volvo, Mercedes, BMW, Audi, Porsche = бизнес,
остальные = обычная 7-местная), это очевидная неточность на границе —
отмечено в отчёте, при необходимости поправить точечно в /admin/.

Категория "Американец (Cadillac/GMC)" против "Американец в целом + Land
Cruiser": первая — только явно названные в прайсе марки (Cadillac, GMC,
Lincoln, Hummer), вторая — прочие большие американские внедорожники
(Chevrolet Tahoe/Suburban, Dodge Durango) и весь модельный ряд Toyota
Land Cruiser. Граница между ними в исходном файле не расписана дословно
(см. предыдущее обсуждение) — это моя интерпретация, требует проверки.

Правила ниже — по паре (марка, базовое имя без указания поколения/года).
Не найденное в словаре имя не трогается (readonly-режим по умолчанию —
см. --apply) и попадает в отчёт как "не классифицировано".

Запуск:
    python manage.py classify_price_categories          # только отчёт
    python manage.py classify_price_categories --apply   # применить к БД
"""

import csv
import re

from django.core.management.base import BaseCommand

from lors.models import CarModel, PriceCategory

# сегмент -> (название категории "с пакетом", название категории "без пакета" или None)
SEGMENT_CATEGORIES = {
    'SEDAN': ('Седан, 5 мест (с пакетом)', 'Седан (без пакета)'),
    'JEEP': ('Джип, 5 мест (с пакетом)', 'Джип (без пакета)'),
    'SEVEN': ('7 мест (с пакетом)', '7 мест, с 7-м рядом (без пакета)'),
    'BUSINESS7': ('7 мест, бизнес (с пакетом)', 'Бизнес (без пакета)'),
    'AMERICAN': ('Американец — Cadillac, GMC и т.п. (с пакетом)', None),
    'LANDCRUISER_AM': ('Американец в целом + Land Cruiser (с пакетом)', None),
    'CARNIVAL': ('Carnival + Staria + H1 (с пакетом)', None),
}

PREMIUM_BRANDS = {
    'Land Rover', 'Lexus', 'Infiniti', 'Genesis', 'Volvo', 'mercedes-Benz', 'BMW', 'Audi', 'Porsche',
}

# явные марки без модельного разбора
BRAND_OVERRIDE = {
    'Cadillac': 'AMERICAN',
    'GMC': 'AMERICAN',
    'Lincoln': 'AMERICAN',
    'Hummer': 'AMERICAN',
}

# (марка, базовое имя без поколения/года) -> сегмент. Не найдено — не трогаем.
MODEL_SEGMENT = {
    # Audi
    ('Audi', 'Audi A3'): 'SEDAN', ('Audi', 'Audi A4'): 'SEDAN', ('Audi', 'Audi A5'): 'SEDAN',
    ('Audi', 'Audi A6'): 'SEDAN', ('Audi', 'Audi A7'): 'SEDAN', ('Audi', 'Audi A8'): 'SEDAN',
    ('Audi', 'Audi TT'): 'SEDAN', ('Audi', 'Audi TT RS'): 'SEDAN', ('Audi', 'Audi e-tron'): 'JEEP',
    ('Audi', 'Audi Q3'): 'JEEP', ('Audi', 'Audi Q5'): 'JEEP',
    ('Audi', 'Audi Q7'): 'BUSINESS7', ('Audi', 'Audi Q8'): 'BUSINESS7',
    # Avatr (EV-кроссоверы)
    ('Avatr', 'avatr 06'): 'SEDAN', ('Avatr', 'avatr 11'): 'JEEP', ('Avatr', 'avatr 12'): 'JEEP',
    # BMW
    ('BMW', 'BMW 1'): 'SEDAN', ('BMW', 'BMW 1 серии'): 'SEDAN', ('BMW', 'BMW 2'): 'SEDAN',
    ('BMW', 'BMW 3'): 'SEDAN', ('BMW', 'BMW 4'): 'SEDAN', ('BMW', 'BMW 5'): 'SEDAN',
    ('BMW', 'BMW 6'): 'SEDAN', ('BMW', 'BMW 6 II sedan'): 'SEDAN', ('BMW', 'BMW 7'): 'SEDAN',
    ('BMW', 'BMW 7 i'): 'SEDAN', ('BMW', 'BMW 7 серии'): 'SEDAN', ('BMW', 'BMW Z4'): 'SEDAN',
    ('BMW', 'BMW i3'): 'SEDAN', ('BMW', 'BMW i8 I Купе'): 'SEDAN',
    ('BMW', 'BMW X1'): 'JEEP', ('BMW', 'BMW X1 s*drive'): 'JEEP', ('BMW', 'BMW iX1 s*drive'): 'JEEP',
    ('BMW', 'BMW X2'): 'JEEP', ('BMW', 'BMW X3'): 'JEEP', ('BMW', 'BMW X4'): 'JEEP',
    ('BMW', 'BMW X5'): 'JEEP', ('BMW', 'BMW X5 M'): 'JEEP', ('BMW', 'BMW X6'): 'JEEP',
    ('BMW', 'BMW X7'): 'BUSINESS7', ('BMW', 'BMW X7 x-drive'): 'BUSINESS7',
    # BYD
    ('BYD', 'BYD DESTROIAR 2025'): 'SEDAN', ('BYD', 'BYD QIN 2025'): 'SEDAN',
    ('BYD', 'BYD selion  2025'): 'SEDAN',
    ('BYD', 'BYD Tang,'): 'SEVEN', ('BYD', 'BYD leopard-7'): 'JEEP',
    ('BYD', 'BYD song plus 2025'): 'JEEP', ('BYD', 'BYD song pro'): 'JEEP', ('BYD', "BYD song'L 2025"): 'JEEP',
    # Cadillac
    ('Cadillac', 'Cadillac escalade'): 'AMERICAN',
    # Changan
    ('Changan', 'Changan Alsvin 2018 - ...'): 'SEDAN', ('Changan', 'Changan Eado Plus 2020 - ...'): 'SEDAN',
    ('Changan', 'Changan Lamore 2023'): 'SEDAN',
    ('Changan', 'Changan CS35'): 'JEEP', ('Changan', 'Changan CS35PLUS I 2018-2023'): 'JEEP',
    ('Changan', 'Changan CS55'): 'JEEP', ('Changan', 'Changan CS55 PLUS'): 'JEEP',
    ('Changan', 'Changan CS75 I Рестайлинг'): 'JEEP', ('Changan', 'Changan CS75PLUS II 2022-2023'): 'JEEP',
    ('Changan', 'Changan CS85COUPE 2019-...'): 'JEEP',
    ('Changan', 'Changan CS95'): 'SEVEN', ('Changan', 'Changan CS95 I 7 мест'): 'SEVEN',
    ('Changan', 'Changan UNI-'): 'JEEP', ('Changan', 'Changan UNI-K'): 'JEEP', ('Changan', 'Changan UNI-T'): 'JEEP',
    # Hunter Plus — пикап, сознательно не классифицируем
    # Chery
    ('Chery', 'Chery Omoda C 5'): 'JEEP', ('Chery', 'Chery Omoda S5'): 'JEEP',
    ('Chery', 'Chery Tiggo'): 'JEEP', ('Chery', 'Chery Tiggo 07'): 'JEEP', ('Chery', 'Chery Tiggo 2'): 'JEEP',
    ('Chery', 'Chery Tiggo 2 pro'): 'JEEP', ('Chery', 'Chery Tiggo 3'): 'JEEP',
    ('Chery', 'Chery Tiggo 4 Рестайлинг'): 'JEEP', ('Chery', 'Chery Tiggo 5'): 'JEEP',
    ('Chery', 'Chery Tiggo 7 Pro Max'): 'JEEP', ('Chery', 'Chery Tiggo 9'): 'JEEP',
    ('Chery', 'Chery Tiggo 8 I 5 мест'): 'JEEP',
    ('Chery', 'Chery Tiggo 8 I 7 мест'): 'SEVEN', ('Chery', 'Chery Tiggo 8 Pro'): 'JEEP',
    ('Chery', 'Chery Tiggo 8 Pro 7 мест'): 'SEVEN', ('Chery', 'Chery Tiggo 8 Pro Max 7 мест'): 'SEVEN',
    ('Chery', 'Chery Tiggo Pro 7'): 'SEVEN',
    # Chevrolet
    ('Chevrolet', 'Chevrolet Aveo'): 'SEDAN', ('Chevrolet', 'Chevrolet Cruze'): 'SEDAN',
    ('Chevrolet', 'Chevrolet Cruze Хэтчбек'): 'SEDAN', ('Chevrolet', 'Chevrolet Epica'): 'SEDAN',
    ('Chevrolet', 'Chevrolet Lacetti'): 'SEDAN', ('Chevrolet', 'Chevrolet Lacetti Универсал'): 'SEDAN',
    ('Chevrolet', 'Chevrolet Lacetti Хэтчбек'): 'SEDAN', ('Chevrolet', 'Chevrolet Lanos'): 'SEDAN',
    ('Chevrolet', 'Chevrolet Malibu'): 'SEDAN', ('Chevrolet', 'Chevrolet Nexia'): 'SEDAN',
    ('Chevrolet', 'Chevrolet Camaro'): 'SEDAN', ('Chevrolet', 'Chevrolet Camaro SS рестайлинг'): 'SEDAN',
    ('Chevrolet', 'Chevrolet Camaro V Купе'): 'SEDAN',
    ('Chevrolet', 'Chevrolet Blazer'): 'JEEP', ('Chevrolet', 'Chevrolet Equinox'): 'JEEP',
    ('Chevrolet', 'Chevrolet TrailBlazer'): 'JEEP',
    ('Chevrolet', 'Chevrolet Captiva'): 'JEEP', ('Chevrolet', 'Chevrolet Captiva Restailing'): 'JEEP',
    ('Chevrolet', 'Chevrolet Captiva 7 мест'): 'SEVEN',
    ('Chevrolet', 'Chevrolet Traverse II кроссовер 7 мест'): 'SEVEN',
    ('Chevrolet', 'Chevrolet Tahoe'): 'LANDCRUISER_AM', ('Chevrolet', 'Chevrolet Tahoe 840'): 'LANDCRUISER_AM',
    ('Chevrolet', 'Chevrolet Tahoe IV 7 мест'): 'LANDCRUISER_AM',
    ('Chevrolet', 'Chevrolet Express'): 'CARNIVAL',
    # Dodge
    ('Dodge', 'Dodge Caliber'): 'SEDAN', ('Dodge', 'Dodge Challenger'): 'SEDAN',
    ('Dodge', 'Dodge Charger'): 'SEDAN',
    ('Dodge', 'Dodge Journey I Рестайлинг'): 'JEEP', ('Dodge', 'Dodge Nitro'): 'JEEP',
    ('Dodge', 'Dodge Durango'): 'LANDCRUISER_AM',
    ('Dodge', 'Dodge Caravan'): 'CARNIVAL', ('Dodge', 'Dodge Grand Caravan'): 'CARNIVAL',
    # FORD (пикапы/Mustang/Explorer)
    ('FORD', 'Ford Mustang'): 'SEDAN', ('FORD', 'ford focus'): 'SEDAN',
    ('FORD', 'Ford Explorer'): 'SEVEN',
    # GMC
    ('GMC', 'gmc yoken denale'): 'AMERICAN',
    # Geely
    ('Geely', 'Geely CK'): 'SEDAN', ('Geely', 'Geely Emgrand 7 I 2016-2020'): 'SEDAN',
    ('Geely', 'Geely Emgrand EC7'): 'SEDAN', ('Geely', 'Geely Emgrand II 2021 - ...'): 'SEDAN',
    ('Geely', 'Geely FC Vision'): 'SEDAN', ('Geely', 'Geely GC 6'): 'SEDAN',
    ('Geely', 'Geely MK'): 'SEDAN', ('Geely', 'Geely MK Cross'): 'SEDAN',
    ('Geely', 'Geely Atlas'): 'JEEP', ('Geely', 'Geely Atlas II 2023 - ...'): 'JEEP',
    ('Geely', 'Geely Coolray'): 'JEEP', ('Geely', 'Geely Coolray I Рестайлинг 2023 - ...'): 'JEEP',
    ('Geely', 'Geely Emgrand X7'): 'JEEP', ('Geely', 'Geely Emgrand X7 I Рестайлинг 2'): 'JEEP',
    ('Geely', 'Geely Icon 2020-...'): 'JEEP', ('Geely', 'Geely Tugella'): 'JEEP',
    ('Geely', 'Geely Monjaro 2021-2023'): 'SEVEN',
    ('Geely', 'Geely Okavango'): 'SEVEN', ('Geely', 'Geely Okavango I Рестайлинг'): 'SEVEN',
    # Genesis
    ('Genesis', 'Genesis g80 2015'): 'SEDAN',
    ('Hyundai', 'Genesis G70'): 'SEDAN', ('Hyundai', 'Genesis G80'): 'SEDAN',
    ('Hyundai', 'Genesis GV80'): 'BUSINESS7',
    # Haval
    ('Haval', 'HAVAL F7'): 'JEEP', ('Haval', 'Haval F7'): 'JEEP',
    ('Haval', 'Haval F7 I Рестайлинг 2022 - ...'): 'JEEP', ('Haval', 'Haval F7x'): 'JEEP',
    ('Haval', 'HAVAL H2'): 'JEEP', ('Haval', 'HAVAL H5'): 'JEEP', ('Haval', 'HAVAL H6'): 'JEEP',
    ('Haval', 'Haval Dargo'): 'JEEP', ('Haval', 'Haval Jolion'): 'JEEP', ('Haval', 'Haval M6'): 'JEEP',
    ('Haval', 'HAVAL H9 5 мест'): 'JEEP', ('Haval', 'HAVAL H9 7 мест'): 'SEVEN',
    # Honda
    ('Honda', 'Honda Accord'): 'SEDAN', ('Honda', 'Honda Accord X 2018-2022'): 'SEDAN',
    ('Honda', 'Honda Civic'): 'SEDAN', ('Honda', 'Honda Civic VI седан'): 'SEDAN',
    ('Honda', 'Honda Civic VI хетчбэк'): 'SEDAN', ('Honda', 'Honda Civic VII 5 дверей'): 'SEDAN',
    ('Honda', 'Honda Civic VII Седан 3d'): 'SEDAN', ('Honda', 'Honda Civic VII хетчбек 3d Левый руль'): 'SEDAN',
    ('Honda', 'Honda Civic VIII 4d'): 'SEDAN', ('Honda', 'Honda Civic VIII 5d'): 'SEDAN',
    ('Honda', 'Honda Civic X Седан 2015-2021'): 'SEDAN', ('Honda', 'Honda Civic X Хэтчбек 2015-2021)'): 'SEDAN',
    ('Honda', 'Honda Jazz'): 'SEDAN',
    ('Honda', 'Honda CR-'): 'JEEP', ('Honda', 'Honda CR-V'): 'JEEP',
    ('Honda', 'Honda HRV I 3d Левый руль'): 'JEEP', ('Honda', 'Honda HRV I 5d Левый руль'): 'JEEP',
    # Hummer
    ('Hummer', 'Hummer H2'): 'AMERICAN', ('Hummer', 'Hummer H3'): 'AMERICAN',
    # Hyundai
    ('Hyundai', 'Hyundai Accent'): 'SEDAN', ('Hyundai', 'Hyundai Avante'): 'SEDAN',
    ('Hyundai', 'Hyundai Azera Grandeur'): 'SEDAN', ('Hyundai', 'Hyundai Coupe'): 'SEDAN',
    ('Hyundai', 'Hyundai Elantra'): 'SEDAN', ('Hyundai', 'Hyundai Equus'): 'SEDAN',
    ('Hyundai', 'Hyundai Genesis Coupe'): 'SEDAN', ('Hyundai', 'Hyundai Genesis G90'): 'SEDAN',
    ('Hyundai', 'Hyundai Genesis l'): 'SEDAN', ('Hyundai', 'Hyundai Genesis ll'): 'SEDAN',
    ('Hyundai', 'Hyundai Getz'): 'SEDAN', ('Hyundai', 'Hyundai Grandeur'): 'SEDAN',
    ('Hyundai', 'Hyundai Grandeur IV Седан'): 'SEDAN', ('Hyundai', 'Hyundai Matrix'): 'SEDAN',
    ('Hyundai', 'Hyundai Solaris'): 'SEDAN', ('Hyundai', 'Hyundai Solaris II Рестайлинг'): 'SEDAN',
    ('Hyundai', 'Hyundai Sonata'): 'SEDAN', ('Hyundai', 'Hyundai Tiburon'): 'SEDAN',
    ('Hyundai', 'Hyundai Veloster'): 'SEDAN', ('Hyundai', 'Hyundai Veloster I Рестайлинг'): 'SEDAN',
    ('Hyundai', 'Hyundai i20'): 'SEDAN', ('Hyundai', 'Hyundai i30'): 'SEDAN',
    ('Hyundai', 'Hyundai i30 III Рестайлинг 2 универсал'): 'SEDAN', ('Hyundai', 'Hyundai i40'): 'SEDAN',
    ('Hyundai', 'Starx'): 'SEDAN',
    ('Hyundai', 'Hyundai Creta I Рестайлинг 1'): 'JEEP', ('Hyundai', 'Hyundai Новая Creta'): 'JEEP',
    ('Hyundai', 'Hyundai Tucson'): 'JEEP', ('Hyundai', 'Hyundai Tucson 2'): 'JEEP',
    ('Hyundai', 'Hyundai Tucson chiki benzin'): 'JEEP', ('Hyundai', 'Hyundai ix35'): 'JEEP',
    ('Hyundai', 'Hyundai kona'): 'JEEP', ('Hyundai', 'Hyundai Santa Cruz'): 'JEEP',
    ('Hyundai', 'Hyundai Santa Fe'): 'SEVEN', ('Hyundai', 'Hyundai Santa Fe III Grand'): 'SEVEN',
    ('Hyundai', 'Hyundai Santa Fe IV Рестайлинг 2020-2023 7 мест'): 'SEVEN',
    ('Hyundai', 'Hyundai Terracan'): 'SEVEN', ('Hyundai', 'Hyundai Terracan I 2001-2004'): 'SEVEN',
    ('Hyundai', 'Hyundai Trajet'): 'SEVEN', ('Hyundai', 'Hyundai ix55'): 'SEVEN',
    ('Hyundai', 'Hyundai ix55 7 мест 2008-2013'): 'SEVEN', ('Hyundai', 'Hyundai ver crus2008-2015'): 'SEVEN',
    ('Hyundai', 'Hyundai Palisade'): 'BUSINESS7', ('Hyundai', 'Hyundai Palisade  7 мест  رجال أعمال'): 'BUSINESS7',
    ('Hyundai', 'رجال أعمال'): 'BUSINESS7',
    ('Hyundai', 'Hyundai Starex'): 'CARNIVAL', ('Hyundai', 'Hyundai Staria'): 'CARNIVAL',
    # Infiniti
    ('Infiniti', 'Infiniti I Q70 седан'): 'SEDAN', ('Infiniti', 'Infiniti M'): 'SEDAN',
    ('Infiniti', 'Infiniti Q50'): 'SEDAN', ('Infiniti', 'Infiniti Q60 II Купе'): 'SEDAN',
    ('Infiniti', 'Infiniti EX'): 'JEEP', ('Infiniti', 'Infiniti FX35'): 'JEEP', ('Infiniti', 'Infiniti FX37'): 'JEEP',
    ('Infiniti', 'Infiniti QX50'): 'JEEP', ('Infiniti', 'Infiniti QX55'): 'JEEP',
    ('Infiniti', 'Infiniti QX56 5 мест'): 'JEEP', ('Infiniti', 'Infiniti QX60 I 5 мест'): 'JEEP',
    ('Infiniti', 'Infiniti QX80 5 мест'): 'JEEP',
    ('Infiniti', 'Infiniti QX56 7 мест'): 'BUSINESS7', ('Infiniti', 'Infiniti QX60 I 7 мест'): 'BUSINESS7',
    ('Infiniti', 'Infiniti QX60 I США 7 мест'): 'BUSINESS7', ('Infiniti', 'Infiniti QX80 7 мест'): 'BUSINESS7',
    ('Infiniti', 'Infiniti QX80 I Рестайлинг 2'): 'BUSINESS7',
    # Isuzu — только D-Max (пикап), не классифицируем
    # Jaecoo / Jaguar
    ('Jaecoo', 'Jaecoo J7 2023 - ...'): 'JEEP',
    ('Jaguar', 'Jaguar xf'): 'SEDAN',
    # Jeep
    ('Jeep', 'Jeep Cherokee'): 'JEEP', ('Jeep', 'Jeep Compass'): 'JEEP',
    ('Jeep', 'Jeep Grand Cherokee'): 'JEEP', ('Jeep', 'Jeep Grand Cherokee 1 Рестайлинг'): 'JEEP',
    ('Jeep', 'eep Grand Cherokee 2 Рестайлинг'): 'JEEP',
    ('Jeep', 'Jeep Renegade I рестайлинг'): 'JEEP', ('Jeep', 'Jeep Renegade Limited 4WD'): 'JEEP',
    ('Jeep', 'Jeep Wrangler'): 'JEEP', ('Jeep', 'Jeep Wrangler Sport'): 'JEEP',
    ('Jeep', 'Jeep Commander 7 мест'): 'SEVEN',
    # Jetour
    ('Jetour', 'Jetour Dashing 2022 - ...'): 'JEEP', ('Jetour', 'Jetour T2'): 'JEEP',
    ('Jetour', 'Jetour X70 PLUS 2020-2023'): 'JEEP', ('Jetour', 'Jetour X90 PLUS 2021 - ...'): 'SEVEN',
    # Kia
    ('Kia', 'KIA Picanto'): 'SEDAN', ('Kia', 'Kia Ceed'): 'SEDAN', ('Kia', 'Kia Cerato'): 'SEDAN',
    ('Kia', 'Kia Cerato Coupe'): 'SEDAN', ('Kia', 'Kia K3'): 'SEDAN', ('Kia', 'Kia K5'): 'SEDAN',
    ('Kia', 'Kia K7'): 'SEDAN', ('Kia', 'Kia K7 hybrid'): 'SEDAN', ('Kia', 'Kia K8 2021 - 2024'): 'SEDAN',
    ('Kia', 'Kia K9'): 'SEDAN', ('Kia', 'Kia Magentis I Рестайлинг'): 'SEDAN',
    ('Kia', 'Kia Magentis II Рестайлинг'): 'SEDAN', ('Kia', 'Kia Optima'): 'SEDAN',
    ('Kia', 'Kia Pride III UB'): 'SEDAN', ('Kia', 'Kia Quoris'): 'SEDAN', ('Kia', 'Kia Rio'): 'SEDAN',
    ('Kia', 'Kia Stinger'): 'SEDAN', ('Kia', 'Kia Venga'): 'SEDAN',
    ('Kia', 'kia forte coupe'): 'SEDAN', ('Kia', 'LADA'): 'SEDAN', ('Kia', 'Kia Soul'): 'JEEP',
    ('Kia', 'Kia Carens'): 'JEEP', ('Kia', 'Kia Niro I 2016-2019'): 'JEEP', ('Kia', 'Kia Seltos'): 'JEEP',
    ('Kia', 'Kia Sportage'): 'JEEP', ('Kia', 'Kia XCeed'): 'JEEP',
    ('Kia', 'Kia Sorento III 5 мест'): 'JEEP', ('Kia', 'Kia Sorento IV 5 мест'): 'JEEP',
    ('Kia', 'Kia Sorento'): 'SEVEN', ('Kia', 'Kia Sorento 2023-2026'): 'SEVEN',
    ('Kia', 'Kia Sorento III 7 мест'): 'SEVEN', ('Kia', 'Kia Sorento IV 6 мест'): 'SEVEN',
    ('Kia', 'Kia Sorento IV 7 мест'): 'SEVEN', ('Kia', 'Kia Sorento Prime'): 'SEVEN',
    ('Kia', 'Kia Sorento hybrid'): 'SEVEN', ('Kia', 'Kia Mohave'): 'SEVEN',
    ('Kia', 'Kia Mohave I Рестайлинг 2 2018-2023 7 мест'): 'SEVEN',
    ('Kia', 'Kia Carnival'): 'CARNIVAL', ('Kia', 'Kia Carnival IV 7 мест'): 'CARNIVAL',
    ('Kia', 'Kia Carnival IV 8 мест'): 'CARNIVAL',
    ('Kia', 'Kia Sedona III 5 мест'): 'CARNIVAL', ('Kia', 'Kia Sedona III 7 мест'): 'CARNIVAL',
    # Kia Bongo — коммерческий, не классифицируем
    # Land Rover
    ('Land Rover', 'Land Rover Defender 110 II 5d'): 'JEEP', ('Land Rover', 'Land Rover Defender 5d'): 'JEEP',
    ('Land Rover', 'Land Rover defender'): 'JEEP', ('Land Rover', 'Land Rover Freelander'): 'JEEP',
    ('Land Rover', 'Land Rover Freelander I 1997-2003'): 'JEEP',
    ('Land Rover', 'Land Rover Range Rover'): 'JEEP', ('Land Rover', 'Land Rover Range Rover Evoque 5d'): 'JEEP',
    ('Land Rover', 'Land Rover Range Rover PHE'): 'JEEP', ('Land Rover', 'Land Rover Range Rover Sport'): 'JEEP',
    ('Land Rover', 'Land Rover Range Rover VOGUE'): 'JEEP', ('Land Rover', 'Land Rover velaar'): 'JEEP',
    ('Land Rover', 'Land Rover Discovery'): 'BUSINESS7', ('Land Rover', 'Land Rover Discovery Sport'): 'BUSINESS7',
    # Lexus
    ('Lexus', 'Lexus CT I Рестайлинг 2014-2018'): 'SEDAN', ('Lexus', 'Lexus ES'): 'SEDAN',
    ('Lexus', 'Lexus ES V Рестайлинг'): 'SEDAN', ('Lexus', 'Lexus GS'): 'SEDAN',
    ('Lexus', 'Lexus HS 250h I Рестайлинг'): 'SEDAN', ('Lexus', 'Lexus IS'): 'SEDAN',
    ('Lexus', 'Lexus IS III F sport'): 'SEDAN', ('Lexus', 'Lexus LS'): 'SEDAN',
    ('Lexus', 'Lexus LS IV long'): 'SEDAN',
    ('Lexus', 'Lexus NX 200'): 'JEEP', ('Lexus', 'Lexus NX 250'): 'JEEP',
    ('Lexus', 'Lexus NX 300 I Рестайлинг 2017-2021'): 'JEEP',
    ('Lexus', 'Lexus GX'): 'JEEP', ('Lexus', 'Lexus GX I 470'): 'JEEP', ('Lexus', 'Lexus GX II Рестайлинг'): 'JEEP',
    ('Lexus', 'Lexus RX'): 'JEEP', ('Lexus', 'Lexus RX 350 V 2022-2023'): 'JEEP',
    ('Lexus', 'Lexus RX III Рестайлинг'): 'JEEP',
    ('Lexus', 'Lexus RX IV 7 мест'): 'BUSINESS7',
    ('Lexus', 'Lexus LX'): 'BUSINESS7', ('Lexus', 'Lexus LX 570'): 'BUSINESS7',
    ('Lexus', 'Lexus LX 570 III 7 мест'): 'BUSINESS7', ('Lexus', 'Lexus LX 570 Рестайлинг'): 'BUSINESS7',
    ('Lexus', 'Lexus LX470'): 'BUSINESS7', ('Lexus', 'Lexus LX570'): 'BUSINESS7',
    # Lincoln
    ('Lincoln', 'Lincoln Navigator'): 'AMERICAN',
    # MG
    ('MG', 'MG'): 'SEDAN', ('MG', 'MG - 5G'): 'SEDAN', ('MG', 'mg rx5'): 'JEEP',
    # Mazda
    ('Mazda', 'Mazda 2'): 'SEDAN', ('Mazda', 'Mazda 3'): 'SEDAN', ('Mazda', 'Mazda 323'): 'SEDAN',
    ('Mazda', 'Mazda 5'): 'SEDAN', ('Mazda', 'Mazda 6'): 'SEDAN', ('Mazda', 'Mazda 626'): 'SEDAN',
    ('Mazda', 'Mazda MX-5'): 'SEDAN', ('Mazda', 'Mazda Premacy'): 'SEDAN', ('Mazda', 'Mazda RX-8'): 'SEDAN',
    ('Mazda', 'Mazda CX-3 I 2015 - ...'): 'JEEP', ('Mazda', 'Mazda CX-30'): 'JEEP',
    ('Mazda', 'Mazda CX-4 I 2016-2019'): 'JEEP', ('Mazda', 'Mazda CX-4 I Рестайлинг 2019 - ...'): 'JEEP',
    ('Mazda', 'Mazda CX-5'): 'JEEP', ('Mazda', 'Mazda CX-7'): 'JEEP',
    ('Mazda', 'Mazda Tribute I Левый руль'): 'JEEP',
    ('Mazda', 'Mazda CX-9'): 'SEVEN', ('Mazda', 'Mazda CX-9 I 7 мест'): 'SEVEN',
    ('Mazda', 'Mazda CX-9 II 5 мест'): 'JEEP', ('Mazda', 'Mazda CX-9 II 7 мест'): 'SEVEN',
    # Mazda Titan/B-Series/Bt-50 — грузовики/пикапы, не классифицируем
    # Mitsubishi
    ('Mitsubishi', 'Mitsubishi 3000 GT'): 'SEDAN', ('Mitsubishi', 'Mitsubishi Carisma'): 'SEDAN',
    ('Mitsubishi', 'Mitsubishi Colt'): 'SEDAN', ('Mitsubishi', 'Mitsubishi Galant'): 'SEDAN',
    ('Mitsubishi', 'Mitsubishi Lancer'): 'SEDAN', ('Mitsubishi', 'Mitsubishi Lancer IX универсал'): 'SEDAN',
    ('Mitsubishi', 'Mitsubishi Lancer X хетчбек'): 'SEDAN', ('Mitsubishi', 'Mitsubishi Space Star'): 'SEDAN',
    ('Mitsubishi', 'Mitsubishi eclips cross 2522'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi AS'): 'JEEP', ('Mitsubishi', 'Mitsubishi ASX'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi Outlander'): 'JEEP', ('Mitsubishi', 'Mitsubishi Outlander III Рестайлинг'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi Outlander III Рестайлинг 2'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi Outlander III 2012-2015 7 мест'): 'SEVEN',
    ('Mitsubishi', 'Mitsubishi Space Wagon'): 'SEVEN',
    ('Mitsubishi', 'Mitsubishi Pajero'): 'JEEP', ('Mitsubishi', 'Mitsubishi Pajero IV 3d'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi Pajero IV 5d'): 'JEEP', ('Mitsubishi', 'Mitsubishi Pajero Pinin'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi montero'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi PAJERO 5.NESİL 2013-202!'): 'SEVEN',
    ('Mitsubishi', 'Mitsubishi Pajero Sport'): 'JEEP', ('Mitsubishi', 'Mitsubishi Pajero Sport III Рестайлинг'): 'JEEP',
    ('Mitsubishi', 'Mitsubishi Pajero Sport III 2015-2021 7 мест'): 'SEVEN',
    # Mitsubishi L200/Fuso Canter — пикап/грузовик, не классифицируем
    # Nissan
    ('Nissan', 'Nissan 350Z I Купе'): 'SEDAN', ('Nissan', 'Nissan Almera'): 'SEDAN',
    ('Nissan', 'Nissan Almera Classic'): 'SEDAN', ('Nissan', 'Nissan Almera Tino'): 'SEDAN',
    ('Nissan', 'Nissan Altima'): 'SEDAN', ('Nissan', 'Nissan Maxima'): 'SEDAN',
    ('Nissan', 'Nissan Maxima Vll'): 'SEDAN', ('Nissan', 'Nissan Micra'): 'SEDAN',
    ('Nissan', 'Nissan Note'): 'SEDAN', ('Nissan', 'Nissan Sentra'): 'SEDAN',
    ('Nissan', 'Nissan Skyline'): 'SEDAN', ('Nissan', 'Nissan Skyline GT-R'): 'SEDAN',
    ('Nissan', 'Nissan Sunny'): 'SEDAN', ('Nissan', 'Nissan Teana'): 'SEDAN',
    ('Nissan', 'Nissan Juke'): 'JEEP', ('Nissan', 'Nissan Murano'): 'JEEP', ('Nissan', 'Nissan Qashqai'): 'JEEP',
    ('Nissan', 'Nissan Qashqai II Рестайлинг'): 'JEEP', ('Nissan', 'Nissan Qashqai II дорестайл'): 'JEEP',
    ('Nissan', 'Nissan Terrano'): 'JEEP', ('Nissan', 'Nissan X-Trail'): 'JEEP', ('Nissan', 'nissan rogue'): 'JEEP',
    ('Nissan', 'Nissan Pathfinder'): 'SEVEN', ('Nissan', 'Nissan Armada'): 'LANDCRUISER_AM',
    ('Nissan', 'Nissan Patrol'): 'LANDCRUISER_AM',
    ('Nissan', 'Nissan Primastar'): 'CARNIVAL', ('Nissan', 'Nissan Serena'): 'CARNIVAL',
    # Nissan Navara — пикап, не классифицируем
    # Peugeot
    ('Peugeot', 'Peugeot 206 2002-2009 hatchback'): 'SEDAN',
    ('Peugeot', 'peugeot 3008 2024-202..'): 'JEEP', ('Peugeot', 'peugeot 5008'): 'SEVEN',
    # Porsche
    ('Porsche', 'Porsche 911'): 'SEDAN', ('Porsche', 'Porsche Cayman'): 'SEDAN',
    ('Porsche', 'Porsche Cayman 718'): 'SEDAN', ('Porsche', 'Porsche Panamera'): 'SEDAN',
    ('Porsche', 'Porsche Cayenne'): 'JEEP', ('Porsche', 'Porsche Cayenne Coupe'): 'JEEP',
    ('Porsche', 'Porsche Macan'): 'JEEP',
    # Renault
    ('Renault', 'Renault jeep'): 'JEEP',
    # SEAT
    ('SEAT', 'SEAT Toledo III 2004-2009'): 'SEDAN', ('SEAT', 'Seat Altea'): 'SEDAN',
    ('SEAT', 'Seat Cordoba II Рестайлинг'): 'SEDAN', ('SEAT', 'Seat Ibiza III рестайлинг хэтчбек'): 'SEDAN',
    ('SEAT', 'Seat Ibiza IV хэтчбэк'): 'SEDAN', ('SEAT', 'Seat Leon'): 'SEDAN',
    ('SEAT', 'Seat Leon I 1999-2006'): 'SEDAN', ('SEAT', 'Seat Ateca'): 'JEEP',
    # Skoda
    ('Skoda', 'Skoda Octavia'): 'SEDAN', ('Skoda', 'Skoda Octavia I Tour'): 'SEDAN',
    ('Skoda', 'Skoda Octavia IV A8 Лифтбек'): 'SEDAN', ('Skoda', 'Skoda Rapid'): 'SEDAN',
    ('Skoda', 'Skoda Rapid I Рестайлинг 2017-2020'): 'SEDAN', ('Skoda', 'Skoda Roomster'): 'SEDAN',
    ('Skoda', 'Skoda Superb'): 'SEDAN',
    ('Skoda', 'Skoda Karoq'): 'JEEP', ('Skoda', 'Skoda Yeti'): 'JEEP',
    ('Skoda', 'Skoda Kodiaq'): 'SEVEN', ('Skoda', 'Skoda Kodiaq I 7 мест'): 'SEVEN',
    # SsangYong
    ('SsangYong', 'SsangYong Istana'): 'CARNIVAL',
    ('SsangYong', 'Ssang Yong Actyon'): 'JEEP', ('SsangYong', 'Ssang Yong Kyron'): 'JEEP',
    ('SsangYong', 'Ssang Yong Tivoli'): 'JEEP',
    ('SsangYong', 'Ssang Yong Rexton'): 'SEVEN', ('SsangYong', 'SsangYong Rexton II Y250'): 'SEVEN',
    ('SsangYong', 'Ssang Yong Stavic'): 'SEVEN', ('SsangYong', 'SsangYong Rodius I Рестайлинг'): 'SEVEN',
    # Ssang Yong Actyon Sport(s) — пикап, не классифицируем
    # Subaru
    ('Subaru', 'Subaru'): 'SEDAN', ('Subaru', 'Subaru Impreza'): 'SEDAN',
    ('Subaru', 'Subaru Impreza II рестайлинг'): 'SEDAN', ('Subaru', 'Subaru Impreza IV Рестайлинг'): 'SEDAN',
    ('Subaru', 'Subaru Legacy'): 'SEDAN', ('Subaru', 'Subaru Legacy I 1989-1994'): 'SEDAN',
    ('Subaru', 'Subaru WRX'): 'SEDAN',
    ('Subaru', 'Subaru Forester'): 'JEEP', ('Subaru', 'Subaru Outback'): 'JEEP', ('Subaru', 'Subaru XV'): 'JEEP',
    # Tesla
    ('Tesla', 'Tesla Model 3'): 'SEDAN', ('Tesla', 'Tesla Model S'): 'SEDAN',
    ('Tesla', 'Tesla Model S I 2012-2016'): 'SEDAN', ('Tesla', 'Tesla Model Y I 2020-2023'): 'JEEP',
    # Toyota
    ('Toyota', 'Toyota Auris'): 'SEDAN', ('Toyota', 'Toyota Avensis'): 'SEDAN',
    ('Toyota', 'Toyota Camry  croz'): 'SEDAN', ('Toyota', 'Toyota Camry XV10'): 'SEDAN',
    ('Toyota', 'Toyota Camry XV20'): 'SEDAN', ('Toyota', 'Toyota Camry XV30'): 'SEDAN',
    ('Toyota', 'Toyota Camry XV40'): 'SEDAN', ('Toyota', 'Toyota Camry XV45'): 'SEDAN',
    ('Toyota', 'Toyota Camry XV50'): 'SEDAN', ('Toyota', 'Toyota Camry XV55'): 'SEDAN',
    ('Toyota', 'Toyota Camry XV70'): 'SEDAN', ('Toyota', 'Toyota Celica'): 'SEDAN',
    ('Toyota', 'Toyota Corolla'): 'SEDAN', ('Toyota', 'Toyota Corolla Verso'): 'SEDAN',
    ('Toyota', 'Toyota Yaris'): 'SEDAN', ('Toyota', 'Toyota Yaris I Рестайлинг'): 'SEDAN',
    ('Toyota', 'Toyota Yaris Verso'): 'SEDAN', ('Toyota', 'Toyota Verso'): 'SEDAN',
    ('Toyota', 'Toyota Verso I 5 мест'): 'SEDAN', ('Toyota', 'Toyota fortuo 2011'): 'SEDAN',
    ('Toyota', 'TOYOTA VELOZ'): 'JEEP', ('Toyota', 'Toyota C-HR'): 'JEEP',
    ('Toyota', 'Toyota C-HR I Рестайлинг'): 'JEEP', ('Toyota', 'Toyota Corolla cross'): 'JEEP',
    ('Toyota', 'Toyota RAV 4'): 'JEEP', ('Toyota', 'Toyota RAV4'): 'JEEP',
    ('Toyota', 'Toyota front lander'): 'JEEP',
    ('Toyota', 'Toyota Land Cruiser Prado'): 'JEEP',
    ('Toyota', 'Toyota Land Cruiser Prado 150 Series Рестайлинг 2'): 'JEEP',
    ('Toyota', 'Toyota Land Cruiser Prado II J90'): 'JEEP', ('Toyota', 'Toyota Land Cruiser Prado II J95'): 'JEEP',
    ('Toyota', 'Toyota Land Cruiser Prado III J120'): 'JEEP', ('Toyota', 'Toyota Land Cruiser Prado IV J150'): 'JEEP',
    ('Toyota', 'Toyota Highlander'): 'SEVEN', ('Toyota', 'Toyota fortuner 2025'): 'SEVEN',
    ('Toyota', 'Toyota Land Cruiser'): 'LANDCRUISER_AM',
    ('Toyota', 'Toyota Land Cruiser 300 5 мест'): 'LANDCRUISER_AM',
    ('Toyota', 'Toyota Land Cruiser 70 Правый руль'): 'LANDCRUISER_AM',
    ('Toyota', 'Toyota Land Cruiser 76'): 'LANDCRUISER_AM',
    ('Toyota', 'Toyota Land Cruiser J100'): 'LANDCRUISER_AM',
    ('Toyota', 'Toyota Land Cruiser J200'): 'LANDCRUISER_AM',
    ('Toyota', 'Toyota Land Cruiser J200 7 мест'): 'LANDCRUISER_AM',
    ('Toyota', 'Toyota Land Cruiser J80 Левый руль'): 'LANDCRUISER_AM',
    # Toyota Hilux/Tundra — пикап, не классифицируем
    # Volkswagen
    ('Volkswagen', 'Volkswagen Beetle'): 'SEDAN', ('Volkswagen', 'Volkswagen Bora'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Golf'): 'SEDAN', ('Volkswagen', 'Volkswagen Golf V plus'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Golf VI plus'): 'SEDAN', ('Volkswagen', 'Volkswagen Golf VII Рестайлинг'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Golf VIII 2020-2025'): 'SEDAN', ('Volkswagen', 'Volkswagen Jetta'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Lupo'): 'SEDAN', ('Volkswagen', 'Volkswagen Passat B3'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Passat B3 Универсал'): 'SEDAN', ('Volkswagen', 'Volkswagen Passat B4'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Passat B4 Универсал'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Passat B5 plus'): 'SEDAN', ('Volkswagen', 'Volkswagen Passat B8'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Passat B8 Универсал'): 'SEDAN', ('Volkswagen', 'Volkswagen Passat В5'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Passat В7'): 'SEDAN', ('Volkswagen', 'Volkswagen Polo'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Scirocco'): 'SEDAN', ('Volkswagen', 'Volkswagen Arteon I Лифтбек'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Arteon I Рестайлинг'): 'SEDAN',
    ('Volkswagen', 'Volkswagen ID.3 I Рестайлинг 2023'): 'SEDAN',
    ('Volkswagen', 'Volkswagen Tiguan'): 'JEEP', ('Volkswagen', 'Volkswagen Touareg'): 'JEEP',
    ('Volkswagen', 'Volkswagen ID.4'): 'JEEP', ('Volkswagen', 'Volkswagen ID.6 Crozz'): 'JEEP',
    ('Volkswagen', 'Volkswagen Touran'): 'SEVEN', ('Volkswagen', 'Volkswagen Teramont I 7мест'): 'BUSINESS7',
    ('Volkswagen', 'Volkswagen Caddy'): 'CARNIVAL', ('Volkswagen', 'Volkswagen Caddy IV 2015-2020'): 'CARNIVAL',
    ('Volkswagen', 'Volkswagen Caravelle T5'): 'CARNIVAL', ('Volkswagen', 'Volkswagen Caravelle T6'): 'CARNIVAL',
    ('Volkswagen', 'Volkswagen Multivan T5'): 'CARNIVAL', ('Volkswagen', 'Volkswagen Multivan T6'): 'CARNIVAL',
    ('Volkswagen', 'Volkswagen Sharan'): 'CARNIVAL',
    ('Volkswagen', 'Volkswagen Sharan I Рестайлинг 2 2003-2010'): 'CARNIVAL',
    ('Volkswagen', 'Volkswagen Sharan II правый руль 7 мест'): 'CARNIVAL',
    ('Volkswagen', 'Volkswagen Transporter T4'): 'CARNIVAL', ('Volkswagen', 'Volkswagen Transporter T5'): 'CARNIVAL',
    ('Volkswagen', 'Volkswagen Transporter T6'): 'CARNIVAL',
    # VW Amarok/Crafter/LT — пикап/грузовик/фургон, не классифицируем
    # Volvo
    ('Volvo', 'Volvo 850'): 'SEDAN', ('Volvo', 'Volvo C30'): 'SEDAN', ('Volvo', 'Volvo S40'): 'SEDAN',
    ('Volvo', 'Volvo S40 I Рестайлинг 1999-2004'): 'SEDAN', ('Volvo', 'Volvo S60'): 'SEDAN',
    ('Volvo', 'Volvo S70 1997-2000'): 'SEDAN', ('Volvo', 'Volvo S80'): 'SEDAN', ('Volvo', 'Volvo S90'): 'SEDAN',
    ('Volvo', 'Volvo V40'): 'SEDAN', ('Volvo', 'Volvo V40 II Рестайлинг 2016-2019'): 'SEDAN',
    ('Volvo', 'Volvo V70 II 2000-2004'): 'SEDAN',
    ('Volvo', 'Volvo XC40'): 'JEEP', ('Volvo', 'Volvo XC60'): 'JEEP', ('Volvo', 'Volvo XC70'): 'JEEP',
    ('Volvo', 'Volvo XC70 II Рестайлинг'): 'JEEP',
    ('Volvo', 'Volvo V90 Cross Country I 2016-2020'): 'JEEP',
    ('Volvo', 'Volvo V90 Cross Country I Рестайлинг 2020-2023'): 'JEEP',
    ('Volvo', 'Volvo XC90'): 'BUSINESS7',
    # fortthing / x peng / DFSK
    ('fortthing', 'forthing  S7'): 'JEEP', ('fortthing', 'forthing friday'): 'SEDAN',
    ('x peng', 'x peng x9'): 'CARNIVAL',
    ('DFSK', 'DFSK seres 3'): 'JEEP',
    # mercedes-Benz (включая MINI, тоже висит на этом Brand в данных)
    ('mercedes-Benz', 'MINI Hatch'): 'SEDAN', ('mercedes-Benz', 'Mini Hatch'): 'SEDAN',
    ('mercedes-Benz', 'Mini Cooper'): 'SEDAN', ('mercedes-Benz', 'Mini Clubman'): 'SEDAN',
    ('mercedes-Benz', 'Mini Countryman'): 'JEEP',
    ('mercedes-Benz', 'Maybach X222'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz A-Class'): 'SEDAN', ('mercedes-Benz', 'mercedes-Benz B-Class'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz B-Класс'): 'SEDAN', ('mercedes-Benz', 'mercedes-Benz C-Class'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz C-Class  w206'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz CL-Class AMG II Купе'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz CLA-Class'): 'SEDAN', ('mercedes-Benz', 'mercedes-Benz CLK-Class'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz CLS 400'): 'SEDAN', ('mercedes-Benz', 'mercedes-Benz CLS-Class'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz E-Class'): 'SEDAN', ('mercedes-Benz', 'mercedes-Benz E-class Coupe'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz S-Class'): 'SEDAN', ('mercedes-Benz', 'mercedes-Benz SLC-класс'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz SLK-Class'): 'SEDAN', ('mercedes-Benz', 'mercedes-Benz Sl-klasse'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-BenzA-Класс'): 'SEDAN', ('mercedes-Benz', 'mercedes-BenzCL-Class'): 'SEDAN',
    ('mercedes-Benz', 'mercedes-Benz GLA'): 'JEEP', ('mercedes-Benz', 'mercedes-Benz GLA-Class'): 'JEEP',
    ('mercedes-Benz', 'mercedes-Benz GLB-Class'): 'JEEP', ('mercedes-Benz', 'mercedes-Benz GLC-Class'): 'JEEP',
    ('mercedes-Benz', 'mercedes-Benz GLC-Class I Рестайлинг'): 'JEEP',
    ('mercedes-Benz', 'mercedes-Benz GLK-Class'): 'JEEP', ('mercedes-Benz', 'mercedes-Benz M-Class'): 'JEEP',
    ('mercedes-Benz', 'mercedes-Benz G-Class'): 'JEEP', ('mercedes-Benz', 'mercedes-Benz EQS SUV 580 2022-...'): 'JEEP',
    ('mercedes-Benz', 'mercedes-Benz GLE-Class'): 'BUSINESS7',
    ('mercedes-Benz', 'mercedes-Benz GLE-class Coupe'): 'JEEP',
    ('mercedes-Benz', 'mercedes-Benz GL-Class'): 'BUSINESS7', ('mercedes-Benz', 'mercedes-Benz GLS'): 'BUSINESS7',
    ('mercedes-Benz', 'mercedes-Benz Maybach GLS 600'): 'BUSINESS7',
    ('mercedes-Benz', 'mercedes-Benz R-Class'): 'CARNIVAL', ('mercedes-Benz', 'mercedes-Benz R-Class 350'): 'CARNIVAL',
    ('mercedes-Benz', 'mercedes-Benz V-Class'): 'CARNIVAL', ('mercedes-Benz', 'mercedes-Benz Viano'): 'CARNIVAL',
    ('mercedes-Benz', 'mercedes-Benz Vito'): 'CARNIVAL',
    # mercedes X-Class/Sprinter/Actros/Atego/814 — пикап/грузовик/фургон, не классифицируем
}


def base_name(name: str) -> str:
    return re.split(r'\s*[IVXLC]+\s*\(|\s*\(', name, maxsplit=1)[0].strip()


class Command(BaseCommand):
    help = 'Разносит CarModel по ценовым категориям на основе марки/модели (Этап 5)'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Записать в БД (по умолчанию — только отчёт)')
        parser.add_argument('--report', default='/tmp/price_category_report.csv', help='Путь для CSV-отчёта')

    def handle(self, *args, **options):
        categories = {name: PriceCategory.objects.get(name=name) for pair in SEGMENT_CATEGORIES.values() for name in pair if name}

        rows = []
        matched = skipped_unknown = skipped_no_tier = 0

        for cm in CarModel.objects.select_related('brand').order_by('brand__name', 'name'):
            brand = cm.brand.name
            key = (brand, base_name(cm.name))
            segment = BRAND_OVERRIDE.get(brand) or MODEL_SEGMENT.get(key)

            if segment is None:
                skipped_unknown += 1
                rows.append([cm.id, brand, cm.name, cm.package, '', 'НЕ НАЙДЕНО В СЛОВАРЕ'])
                continue

            with_pkg, without_pkg = SEGMENT_CATEGORIES[segment]
            use_without = cm.package == 'لايوجد باكاج' and without_pkg
            target_name = without_pkg if use_without else with_pkg

            if target_name is None:
                skipped_no_tier += 1
                rows.append([cm.id, brand, cm.name, cm.package, segment, 'НЕТ ТАРИФА "БЕЗ ПАКЕТА" ДЛЯ ЭТОГО СЕГМЕНТА'])
                continue

            rows.append([cm.id, brand, cm.name, cm.package, segment, target_name])
            matched += 1
            if options['apply']:
                cm.price_category = categories[target_name]
                cm.save(update_fields=['price_category'])

        with open(options['report'], 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'марка', 'модель', 'package (каталог)', 'сегмент', 'итоговая категория / статус'])
            writer.writerows(rows)

        self.stdout.write(self.style.SUCCESS(
            f'Классифицировано: {matched}, не найдено в словаре: {skipped_unknown}, '
            f'без тарифа "без пакета" для сегмента: {skipped_no_tier}',
        ))
        self.stdout.write(f'Отчёт: {options["report"]}')
        if not options['apply']:
            self.stdout.write(self.style.WARNING('Режим отчёта — в БД ничего не записано. Запустите с --apply.'))
