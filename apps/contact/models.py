from django.db import models
from apps.core.models import BaseModel


class ContactMessage(BaseModel):
    """Сообщения с формы обратной связи"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Телефон", blank=True)
    company = models.CharField(max_length=200, verbose_name="Компания", blank=True)
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    
    # Статус обработки
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('completed', 'Обработано'),
        ('archived', 'Архивировано'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name="Статус"
    )
    
    # Дополнительные поля
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес", null=True, blank=True)
    user_agent = models.TextField(verbose_name="User Agent", blank=True)
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    @property
    def status_display_class(self):
        """CSS класс для отображения статуса"""
        status_classes = {
            'new': 'status-new',
            'in_progress': 'status-progress',
            'completed': 'status-completed',
            'archived': 'status-archived',
        }
        return status_classes.get(self.status, 'status-new')
