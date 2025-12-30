from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django import forms
from .models import CompanyInfo, KeyFigure, Client, Certificate, License, HomeService, HomeProjectImage, WhoWeAreImage


class LicenseAdminForm(forms.ModelForm):
    class Meta:
        model = License
        fields = '__all__'
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file and not self.instance.pk:
            raise ValidationError('Файл обязателен для загрузки')
        if not file and self.instance.pk:
            # Если редактируем существующий объект и файл не загружен, оставляем старый
            return self.instance.file
        return file


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'founded_year', 'phone', 'email', 'is_active']
    list_filter = ['is_active', 'founded_year']
    search_fields = ['name', 'phone', 'email']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'short_description', 'full_description', 'founded_year')
        }),
        ('О компании', {
            'fields': ('mission', 'vision', 'values')
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'address_almaty', 'address_atyrau', 'working_hours')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        })
    )


@admin.register(KeyFigure)
class KeyFigureAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'description', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['logo_preview', 'website', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['website']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    fieldsets = (
        ('Партнер', {
            'fields': ('logo', 'website', 'order', 'is_active')
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: contain;" />', obj.logo.url)
        return "Нет изображения"
    logo_preview.short_description = "Логотип"


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'number', 'issue_date', 'expiry_date', 'issuer', 'is_valid_display', 'is_active']
    list_filter = ['is_active', 'issue_date', 'expiry_date', 'issuer']
    search_fields = ['title', 'number', 'issuer']
    date_hierarchy = 'issue_date'
    ordering = ['-issue_date']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'number', 'issuer'),
            'description': 'Заполните основную информацию о сертификате. Все поля обязательны для заполнения.'
        }),
        ('Даты', {
            'fields': ('issue_date', 'expiry_date'),
            'description': 'Укажите дату выдачи сертификата. Дата окончания можно оставить пустой для бессрочных сертификатов.'
        }),
        ('Изображение', {
            'fields': ('image',),
            'description': 'Загрузите изображение сертификата. Рекомендуемый формат: JPG или PNG, размер не менее 800x1000 пикселей.'
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order'),
            'description': 'Используйте "Порядок сортировки" для управления порядком отображения сертификатов на сайте (0 - первый, 1 - второй и т.д.).'
        }),
    )
    
    def is_valid_display(self, obj):
        if obj.is_valid:
            return format_html('<span style="color: green;">✓ Действителен</span>')
        else:
            return format_html('<span style="color: red;">✗ Истек</span>')
    is_valid_display.short_description = "Статус"


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    form = LicenseAdminForm
    list_display = ['file_preview', 'title', 'file_type_display', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    fieldsets = (
        ('Лицензия', {
            'fields': ('title', 'file', 'order', 'is_active'),
            'description': 'Можно загрузить изображение (JPG, PNG, GIF) или PDF файл'
        }),
    )
    
    def file_preview(self, obj):
        if obj.file:
            if obj.is_image():
                return format_html('<img src="{}" width="150" height="200" style="object-fit: contain;" />', obj.file.url)
            elif obj.is_pdf():
                return format_html(
                    '<div style="width:150px; height:200px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border:1px solid #ddd;">'
                    '<span style="font-size:3rem;">📄</span><br>'
                    '<span style="font-size:0.8rem; margin-top:10px;">PDF</span>'
                    '</div>'
                )
        return "Нет файла"
    file_preview.short_description = "Превью"
    
    def file_type_display(self, obj):
        if obj.file:
            if obj.is_image():
                return format_html('<span style="color: green;">🖼️ Изображение</span>')
            elif obj.is_pdf():
                return format_html('<span style="color: blue;">📄 PDF</span>')
        return "-"
    file_type_display.short_description = "Тип файла"


@admin.register(HomeService)
class HomeServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description_preview', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Иконка', {
            'fields': ('icon_svg',),
            'description': 'Вставьте SVG код иконки. Если не указано, будет использована стандартная иконка.'
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        })
    )
    
    def description_preview(self, obj):
        if obj.description:
            preview = obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
            return preview
        return "-"
    description_preview.short_description = "Описание"


@admin.register(HomeProjectImage)
class HomeProjectImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    fieldsets = (
        ('Изображение проекта', {
            'fields': ('title', 'image', 'order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = "Превью"


@admin.register(WhoWeAreImage)
class WhoWeAreImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    fieldsets = (
        ('Изображение для секции "КТО МЫ"', {
            'fields': ('title', 'image', 'order', 'is_active'),
            'description': 'Загрузите изображения для отображения в секции "КТО МЫ" на главной странице. Рекомендуется загружать 4 изображения.'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = "Превью"
