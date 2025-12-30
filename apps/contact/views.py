from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .forms import ContactForm
from apps.core.models import CompanyInfo


class ContactView(TemplateView):
    """Страница контактов"""
    template_name = 'contact/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        
        try:
            context['company'] = CompanyInfo.objects.filter(is_active=True).first()
        except CompanyInfo.DoesNotExist:
            context['company'] = None
        
        context['page_title'] = 'Контакты'
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Сохраняем сообщение
            contact_message = form.save(commit=False)
            contact_message.ip_address = self.get_client_ip(request)
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            
            # Отправляем уведомление (опционально)
            try:
                self.send_notification_email(contact_message)
            except Exception as e:
                pass  # Не прерываем процесс, если email не отправился
            
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact:contact')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
    
    def get_client_ip(self, request):
        """Получение IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def send_notification_email(self, contact_message):
        """Отправка уведомления о новом сообщении"""
        subject = f'Новое сообщение с сайта: {contact_message.subject}'
        message = f'''
        Новое сообщение с сайта Poligram:
        
        Имя: {contact_message.name}
        Email: {contact_message.email}
        Телефон: {contact_message.phone}
        Компания: {contact_message.company}
        Тема: {contact_message.subject}
        
        Сообщение:
        {contact_message.message}
        
        IP адрес: {contact_message.ip_address}
        Дата: {contact_message.created_at}
        '''
        
        # Здесь можно настроить отправку email
        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     ['admin@poligram.kz'],  # Email администратора
        #     fail_silently=True,
        # )
