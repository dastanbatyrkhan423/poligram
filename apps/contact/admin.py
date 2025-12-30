from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'status_colored', 'created_at']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message', 'company']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Информация о контакте', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Сообщение', {
            'fields': ('subject', 'message')
        }),
        ('Обработка', {
            'fields': ('status',)
        }),
        ('Техническая информация', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def status_colored(self, obj):
        colors = {
            'new': '#dc3545',
            'in_progress': '#ffc107', 
            'completed': '#28a745',
            'archived': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = "Статус"
    
    actions = ['mark_as_in_progress', 'mark_as_completed', 'mark_as_archived']
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f"Статус {queryset.count()} сообщений изменен на 'В обработке'")
    mark_as_in_progress.short_description = "Отметить как 'В обработке'"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"Статус {queryset.count()} сообщений изменен на 'Обработано'")
    mark_as_completed.short_description = "Отметить как 'Обработано'"
    
    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
        self.message_user(request, f"Статус {queryset.count()} сообщений изменен на 'Архивировано'")
    mark_as_archived.short_description = "Архивировать"
