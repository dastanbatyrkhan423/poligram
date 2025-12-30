from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class BaseModel(models.Model):
    """Базовая модель с общими полями"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        abstract = True
        ordering = ['order', '-created_at']


class CompanyInfo(BaseModel):
    """Информация о компании"""
    name = models.CharField(max_length=200, verbose_name="Название компании")
    short_description = RichTextField(verbose_name="Краткое описание")
    full_description = RichTextField(verbose_name="Полное описание")
    founded_year = models.PositiveIntegerField(verbose_name="Год основания")
    mission = RichTextField(verbose_name="Миссия", blank=True)
    vision = RichTextField(verbose_name="Видение", blank=True)
    values = RichTextField(verbose_name="Ценности", blank=True)
    
    # Контактная информация
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address_almaty = models.TextField(verbose_name="Адрес в Алматы")
    address_atyrau = models.TextField(verbose_name="Адрес в Атырау", blank=True)
    working_hours = models.CharField(max_length=100, verbose_name="Режим работы")
    
    # SEO
    meta_title = models.CharField(max_length=200, verbose_name="Meta Title", blank=True)
    meta_description = models.TextField(verbose_name="Meta Description", blank=True)
    
    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"
    
    def __str__(self):
        return self.name


class KeyFigure(BaseModel):
    """Ключевые цифры компании"""
    title = models.CharField(max_length=100, verbose_name="Название")
    value = models.CharField(max_length=50, verbose_name="Значение")
    description = models.CharField(max_length=200, verbose_name="Описание")
    icon = models.CharField(max_length=50, verbose_name="Иконка (emoji)", blank=True)
    
    class Meta:
        verbose_name = "Ключевая цифра"
        verbose_name_plural = "Ключевые цифры"
    
    def __str__(self):
        return f"{self.title}: {self.value}"


class Client(BaseModel):
    """Партнеры компании"""
    logo = models.ImageField(upload_to='clients/', verbose_name="Логотип партнера")
    logo_thumbnail = ImageSpecField(
        source='logo',
        processors=[ResizeToFill(200, 100)],
        format='PNG',
        options={'quality': 90}
    )
    website = models.URLField(verbose_name="Ссылка на сайт", blank=True)
    
    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Наши партнеры"
    
    def __str__(self):
        if self.pk:
            return f"Партнер {self.pk}"
        return "Новый партнер"


class Certificate(BaseModel):
    """Сертификаты компании"""
    title = models.CharField(
        max_length=200, 
        verbose_name="Название сертификата",
        help_text="Например: Лицензия на строительно-монтажные работы 1 категории"
    )
    number = models.CharField(
        max_length=100, 
        verbose_name="Номер сертификата",
        help_text="Например: KZ.16.01.01.001.Е.000001.01.06"
    )
    issue_date = models.DateField(
        verbose_name="Дата выдачи",
        help_text="Дата, когда был выдан сертификат (формат: ДД.ММ.ГГГГ)"
    )
    expiry_date = models.DateField(
        verbose_name="Дата окончания", 
        null=True, 
        blank=True,
        help_text="Оставьте пустым, если сертификат бессрочный"
    )
    issuer = models.CharField(
        max_length=200, 
        verbose_name="Выдавший орган",
        help_text="Например: Министерство индустрии и инфраструктурного развития РК"
    )
    image = models.ImageField(
        upload_to='certificates/', 
        verbose_name="Изображение сертификата",
        help_text="Загрузите изображение сертификата (JPG, PNG). Рекомендуемый размер: не менее 800x1000 пикселей"
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 400)],
        format='JPEG',
        options={'quality': 90}
    )
    
    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"
    
    def __str__(self):
        return self.title
    
    @property
    def is_valid(self):
        """Проверка действительности сертификата"""
        if not self.expiry_date:
            return True
        from django.utils import timezone
        return timezone.now().date() <= self.expiry_date


class License(BaseModel):
    """Лицензии компании"""
    title = models.CharField(max_length=200, verbose_name="Название лицензии", blank=True)
    file = models.FileField(upload_to='licenses/', verbose_name="Файл лицензии (изображение или PDF)", blank=True, null=True)
    
    class Meta:
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"
    
    def __str__(self):
        return self.title if self.title else f"Лицензия {self.pk}"
    
    def is_image(self):
        """Проверка, является ли файл изображением"""
        if not self.file:
            return False
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        return any(self.file.name.lower().endswith(ext) for ext in image_extensions)
    
    def is_pdf(self):
        """Проверка, является ли файл PDF"""
        if not self.file:
            return False
        return self.file.name.lower().endswith('.pdf')
    
    def get_file_type(self):
        """Возвращает тип файла: 'image', 'pdf' или 'unknown'"""
        if self.is_image():
            return 'image'
        elif self.is_pdf():
            return 'pdf'
        return 'unknown'


class HomeService(BaseModel):
    """Услуги для секции 'Наши услуги' на главной странице"""
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL (для якорной ссылки)", blank=True)
    description = models.TextField(verbose_name="Описание услуги")
    icon_svg = models.TextField(
        verbose_name="SVG код иконки", 
        blank=True,
        help_text="Вставьте SVG код иконки. Если не указано, будет использована стандартная иконка."
    )
    
    class Meta:
        verbose_name = "Услуга на главной"
        verbose_name_plural = "Услуги на главной"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class HomeProjectImage(BaseModel):
    """Изображения проектов для секции 'ИНДИВИДУАЛЬНЫЕ СТРОИТЕЛЬНЫЕ РЕШЕНИЯ' на главной странице"""
    title = models.CharField(max_length=200, verbose_name="Название проекта", blank=True)
    image = models.ImageField(upload_to='home_projects/', verbose_name="Изображение проекта")
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 90}
    )
    
    class Meta:
        verbose_name = "Изображение проекта на главной"
        verbose_name_plural = "Изображения проектов на главной"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title or f"Проект {self.id}"


class WhoWeAreImage(BaseModel):
    """Изображения для секции 'КТО МЫ' на главной странице"""
    title = models.CharField(max_length=200, verbose_name="Название изображения", blank=True)
    image = models.ImageField(upload_to='who_we_are/', verbose_name="Изображение")
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 90}
    )
    
    class Meta:
        verbose_name = "Изображение для секции 'КТО МЫ'"
        verbose_name_plural = "Изображения для секции 'КТО МЫ'"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title or f"Изображение {self.id}"
