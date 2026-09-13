from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE_MB = 8


def validate_image_size(image):
    """Throttle (см. views.py) режет число запросов, но не мешает одному
    запросу принести гигантский файл — например, один POST с фото на
    сотни МБ. Без этого ограничения такой запрос проходил бы (при условии
    что укладывается в throttle) и заполнял диск сервера."""
    if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f'Файл больше {MAX_IMAGE_SIZE_MB} МБ.')
