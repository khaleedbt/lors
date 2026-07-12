from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=255)
    template_code = models.CharField('код шаблона', max_length=50, blank=True)
    car_type = models.CharField('тип автомобиля', max_length=255, blank=True)
    driver_cut = models.CharField('шофёр', max_length=255, blank=True)
    package = models.CharField('пакет', max_length=255, blank=True)
    second_row_package = models.CharField('пакет 2-й ряд', max_length=255, blank=True)
    notes = models.TextField('примечания', blank=True)
    video_url = models.URLField('ссылка на видео', max_length=500, blank=True)
    sheet_row = models.PositiveIntegerField('строка в исходной таблице', unique=True, null=True, blank=True)

    class Meta:
        ordering = ['brand__name', 'name']

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class Complaint(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (STATUS_NEW, 'новая'),
        (STATUS_IN_PROGRESS, 'в работе'),
        (STATUS_RESOLVED, 'решена'),
    ]

    car_model = models.ForeignKey(
        CarModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints',
    )
    name = models.CharField('имя', max_length=150)
    phone = models.CharField('телефон', max_length=32)
    text = models.TextField('текст жалобы')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'


class ComplaintPhoto(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='complaints/%Y/%m/')


class SiteSettings(models.Model):
    address = models.CharField('адрес', max_length=500, blank=True)
    latitude = models.DecimalField('широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('долгота', max_digits=9, decimal_places=6, null=True, blank=True)
    about = models.TextField('о компании', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    whatsapp_url = models.URLField('WhatsApp', blank=True)

    class Meta:
        verbose_name = 'настройки сайта'
        verbose_name_plural = 'настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
