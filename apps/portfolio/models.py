from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from apps.core.models import BaseModel, Client
from apps.services.models import Service


class Project(BaseModel):
    """Проекты портфолио"""
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='projects',
        verbose_name="Клиент"
    )
    services = models.ManyToManyField(
        Service,
        related_name='projects',
        verbose_name="Услуги",
        blank=True
    )
    
    # Основная информация
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = RichTextField(verbose_name="Полное описание")
    year = models.PositiveIntegerField(verbose_name="Год реализации")
    location = models.CharField(max_length=200, verbose_name="Местоположение")
    
    # Статус проекта
    STATUS_CHOICES = [
        ('completed', 'Завершен'),
        ('in_progress', 'В процессе'),
        ('planned', 'Планируется'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='completed',
        verbose_name="Статус"
    )
    
    # Объем работ
    scope_of_work = RichTextField(verbose_name="Объем работ", blank=True)
    
    # Основное изображение
    main_image = models.ImageField(upload_to='projects/', verbose_name="Основное изображение")
    main_image_thumbnail = ImageSpecField(
        source='main_image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 90}
    )
    main_image_small = ImageSpecField(
        source='main_image',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 85}
    )
    
    # Флаги
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый проект")
    
    # SEO
    meta_title = models.CharField(max_length=200, verbose_name="Meta Title", blank=True)
    meta_description = models.TextField(verbose_name="Meta Description", blank=True)
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['-year', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})
    
    @property
    def status_display_class(self):
        """CSS класс для отображения статуса"""
        status_classes = {
            'completed': 'status-completed',
            'in_progress': 'status-progress',
            'planned': 'status-planned',
        }
        return status_classes.get(self.status, 'status-completed')


class ProjectImage(BaseModel):
    """Фотогалерея проектов"""
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Проект"
    )
    image = models.ImageField(upload_to='projects/gallery/', verbose_name="Изображение")
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 90}
    )
    image_large = ImageSpecField(
        source='image',
        processors=[ResizeToFill(800, 600)],
        format='JPEG',
        options={'quality': 95}
    )
    title = models.CharField(max_length=200, verbose_name="Название", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    
    class Meta:
        verbose_name = "Изображение проекта"
        verbose_name_plural = "Изображения проектов"
    
    def __str__(self):
        return f"{self.project.title} - {self.title or 'Изображение'}"


class ProjectCategory(BaseModel):
    """Категории проектов для фильтрации"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    projects = models.ManyToManyField(
        Project,
        related_name='categories',
        verbose_name="Проекты",
        blank=True
    )
    
    class Meta:
        verbose_name = "Категория проектов"
        verbose_name_plural = "Категории проектов"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
