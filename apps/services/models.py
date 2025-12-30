from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from apps.core.models import BaseModel


class ServiceCategory(BaseModel):
    """Категории услуг"""
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description = RichTextField(verbose_name="Описание", blank=True)
    icon = models.CharField(max_length=50, verbose_name="Иконка (emoji)", blank=True)
    image = models.ImageField(upload_to='service_categories/', verbose_name="Изображение", blank=True)
    
    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('services:category_detail', kwargs={'slug': self.slug})


class Service(BaseModel):
    """Услуги компании"""
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.CASCADE, 
        related_name='services',
        verbose_name="Категория"
    )
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = RichTextField(verbose_name="Полное описание")
    competencies = RichTextField(verbose_name="Компетенции", blank=True)
    software = RichTextField(verbose_name="Программное обеспечение", blank=True)
    experience = RichTextField(verbose_name="Опыт работы", blank=True)
    
    # Изображения
    main_image = models.ImageField(upload_to='services/', verbose_name="Основное изображение", blank=True)
    main_image_thumbnail = ImageSpecField(
        source='main_image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 90}
    )
    
    # SEO
    meta_title = models.CharField(max_length=200, verbose_name="Meta Title", blank=True)
    meta_description = models.TextField(verbose_name="Meta Description", blank=True)
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.slug})


class ServiceImage(BaseModel):
    """Дополнительные изображения для услуг"""
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Услуга"
    )
    image = models.ImageField(upload_to='services/gallery/', verbose_name="Изображение")
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 90}
    )
    title = models.CharField(max_length=200, verbose_name="Название", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    
    class Meta:
        verbose_name = "Изображение услуги"
        verbose_name_plural = "Изображения услуг"
    
    def __str__(self):
        return f"{self.service.name} - {self.title or 'Изображение'}"
