from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceCategory, Service, ServiceImage


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ['image', 'title', 'description', 'order', 'is_active']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'image_preview', 'order', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'short_description', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    ordering = ['category', 'order']
    inlines = [ServiceImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'short_description', 'main_image')
        }),
        ('Детальная информация', {
            'fields': ('full_description', 'competencies', 'software', 'experience')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        })
    )
    
    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="50" height="38" style="object-fit: cover;" />', obj.main_image.url)
        return "Нет изображения"
    image_preview.short_description = "Изображение"


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'title', 'image_preview', 'order', 'is_active']
    list_filter = ['is_active', 'service__category']
    search_fields = ['title', 'description', 'service__name']
    list_editable = ['order', 'is_active']
    ordering = ['service', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="38" style="object-fit: cover;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = "Изображение"
