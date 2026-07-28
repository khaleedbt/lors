from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'марка'
        verbose_name_plural = 'марки'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPE_CHOICES = [
        ('تكسي عادي', 'تكسي عادي'),
        ('خمس أبواب (هاش باك)', 'خمس أبواب (هاش باك)'),
        ('ثلاث أبواب (هاش باك)', 'ثلاث أبواب (هاش باك)'),
        ('بابين (كوبي)', 'بابين (كوبي)'),
        ('كوبي بابين', 'كوبي بابين'),
        ('اربع ابواب (كوبي)', 'اربع ابواب (كوبي)'),
        ('بيك آب', 'بيك آب'),
        ('باكاج طويل', 'باكاج طويل'),
    ]
    DRIVER_CUT_CHOICES = [
        ('دعسة مقصوصة', 'دعسة مقصوصة'),
        ('دعسة من تحت', 'دعسة من تحت'),
        ('بدون دعسة', 'بدون دعسة'),
        ('3D', '3D'),
    ]
    PACKAGE_CHOICES = [
        ('قطعة واحدة', 'قطعة واحدة'),
        ('2 قطع', '2 قطع'),
        ('3 قطع', '3 قطع'),
        ('أربع قطع', 'أربع قطع'),
        ('لايوجد باكاج', 'لايوجد باكاج'),
    ]
    SECOND_ROW_PACKAGE_CHOICES = [
        ('قطعة واحدة', 'قطعة واحدة'),
        ('2 قطع', '2 قطع'),
        ('3 قطع', '3 قطع'),
        ('قطعة واحدة + 3 قطع', 'قطعة واحدة + 3 قطع'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=255)
    template_code = models.CharField('код шаблона', max_length=50, blank=True)
    car_type = models.CharField('тип автомобиля', max_length=255, choices=CAR_TYPE_CHOICES, blank=True)
    driver_cut = models.CharField('шофёр', max_length=255, choices=DRIVER_CUT_CHOICES, blank=True)
    package = models.CharField('пакет', max_length=255, choices=PACKAGE_CHOICES, blank=True)
    second_row_package = models.CharField(
        'пакет 2-й ряд', max_length=255, choices=SECOND_ROW_PACKAGE_CHOICES, blank=True,
    )
    notes = models.TextField('примечания', blank=True)
    video_url = models.URLField('ссылка на видео', max_length=500, blank=True)
    sheet_row = models.PositiveIntegerField('строка в исходной таблице', unique=True, null=True, blank=True)

    class Meta:
        ordering = ['brand__name', 'name']
        verbose_name = 'модель автомобиля'
        verbose_name_plural = 'модели автомобилей'

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class Material(models.Model):
    name = models.CharField('название', max_length=100)
    order = models.PositiveIntegerField('порядок', default=0)
    is_active = models.BooleanField('активен', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField('название', max_length=100)
    hex_code = models.CharField('HEX-код', max_length=7, blank=True)
    order = models.PositiveIntegerField('порядок', default=0)
    is_active = models.BooleanField('активен', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'цвет'
        verbose_name_plural = 'цвета'

    def __str__(self):
        return self.name


class MatSetPrice(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='mat_set_prices')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['material__order']
        unique_together = [('car_model', 'material')]
        verbose_name = 'цена комплекта'
        verbose_name_plural = 'цены комплектов'

    def __str__(self):
        return f'{self.car_model} × {self.material}: {self.price}'


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=100, unique=True)
    order = models.PositiveIntegerField('порядок', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'категория товара'
        verbose_name_plural = 'категории товаров'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products',
    )
    name = models.CharField('название', max_length=255)
    description = models.TextField('описание', blank=True)
    is_active = models.BooleanField('активен', default=True)
    order = models.PositiveIntegerField('порядок', default=0)

    class Meta:
        ordering = ['category__order', 'order', 'name']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField('размер', max_length=50, blank=True)
    color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_variants',
    )
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    image = models.ImageField('фото', upload_to='products/%Y/%m/', blank=True)
    is_active = models.BooleanField('активен', default=True)
    order = models.PositiveIntegerField('порядок', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'вариант товара'
        verbose_name_plural = 'варианты товара'

    def __str__(self):
        parts = [self.product.name, self.size, self.color.name if self.color else '']
        return ' — '.join(p for p in parts if p)


class Lead(models.Model):
    TYPE_COMPLAINT = 'complaint'
    TYPE_MAT_ORDER = 'mat_order'
    TYPE_PRODUCT_ORDER = 'product_order'
    TYPE_CHOICES = [
        (TYPE_COMPLAINT, 'жалоба'),
        (TYPE_MAT_ORDER, 'заказ коврика'),
        (TYPE_PRODUCT_ORDER, 'заказ товара'),
    ]

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (STATUS_NEW, 'новая'),
        (STATUS_IN_PROGRESS, 'в работе'),
        (STATUS_RESOLVED, 'решена'),
    ]

    lead_type = models.CharField('тип заявки', max_length=20, choices=TYPE_CHOICES, default=TYPE_COMPLAINT)
    name = models.CharField('имя', max_length=150)
    phone = models.CharField('телефон', max_length=32)
    text = models.TextField('текст', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    # заказ коврика (TYPE_MAT_ORDER)
    car_model = models.ForeignKey(
        CarModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads',
    )
    material = models.ForeignKey(
        Material, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads',
    )
    mat_color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='mat_color_leads',
    )
    border_color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='border_color_leads',
    )
    heel_color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='heel_color_leads',
    )

    # заказ товара (TYPE_PRODUCT_ORDER)
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'{self.get_lead_type_display()}: {self.name} ({self.get_status_display()})'


class LeadPhoto(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='leads/%Y/%m/')

    class Meta:
        verbose_name = 'фото заявки'
        verbose_name_plural = 'фото заявки'


class Review(models.Model):
    RATING_CHOICES = [(n, str(n)) for n in range(1, 6)]

    SOURCE_SITE = 'site'
    SOURCE_GOOGLE = 'google'
    SOURCE_CHOICES = [
        (SOURCE_SITE, 'сайт'),
        (SOURCE_GOOGLE, 'Google'),
    ]

    name = models.CharField('имя', max_length=150)
    text = models.TextField('текст отзыва')
    rating = models.PositiveSmallIntegerField('рейтинг', choices=RATING_CHOICES, default=5)
    source = models.CharField('источник', max_length=20, choices=SOURCE_CHOICES, default=SOURCE_SITE)
    photo = models.ImageField('фото', upload_to='reviews/%Y/%m/', blank=True)
    is_published = models.BooleanField('опубликован', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.name


class SiteSettings(models.Model):
    address = models.CharField('адрес', max_length=500, blank=True)
    latitude = models.DecimalField('широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('долгота', max_digits=9, decimal_places=6, null=True, blank=True)
    about = models.TextField('о компании', blank=True)

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


class Contact(models.Model):
    TYPE_PHONE = 'phone'
    TYPE_INSTAGRAM = 'instagram'
    TYPE_TELEGRAM = 'telegram'
    TYPE_WHATSAPP = 'whatsapp'
    TYPE_FACEBOOK = 'facebook'
    TYPE_YOUTUBE = 'youtube'
    TYPE_CHOICES = [
        (TYPE_PHONE, 'Телефон'),
        (TYPE_INSTAGRAM, 'Instagram'),
        (TYPE_TELEGRAM, 'Telegram'),
        (TYPE_WHATSAPP, 'WhatsApp'),
        (TYPE_FACEBOOK, 'Facebook'),
        (TYPE_YOUTUBE, 'YouTube'),
    ]

    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField('тип', max_length=20, choices=TYPE_CHOICES)
    label = models.CharField('подпись', max_length=100, blank=True)
    value = models.CharField('значение', max_length=255)
    order = models.PositiveIntegerField('порядок', default=0)

    class Meta:
        ordering = ['contact_type', 'order', 'id']
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'

    def __str__(self):
        label = f' ({self.label})' if self.label else ''
        return f'{self.get_contact_type_display()}{label}: {self.value}'


class Page(models.Model):
    slug = models.SlugField('слаг', max_length=100, unique=True)
    title = models.CharField('заголовок', max_length=255)
    body = models.TextField('текст', blank=True)
    image = models.ImageField('изображение', upload_to='pages/%Y/%m/', blank=True)
    updated_at = models.DateTimeField('обновлено', auto_now=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'

    def __str__(self):
        return self.title
