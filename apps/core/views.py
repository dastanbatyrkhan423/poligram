from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .models import CompanyInfo, KeyFigure, Client, Certificate, License, HomeService, HomeProjectImage, WhoWeAreImage
from apps.services.models import Service, ServiceCategory, ServiceImage
# from apps.portfolio.models import Project  # Портфолио отключено


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Информация о компании
        try:
            context['company'] = CompanyInfo.objects.filter(is_active=True).first()
        except CompanyInfo.DoesNotExist:
            context['company'] = None
        
        # Ключевые цифры
        context['key_figures'] = KeyFigure.objects.filter(is_active=True)[:4]
        
        # Категории услуг для больших карточек (первые 4)
        categories = ServiceCategory.objects.filter(is_active=True).order_by('order')[:4]
        context['service_categories'] = categories
        
        # По одной услуге из каждой категории для секции "ИНДИВИДУАЛЬНЫЕ СТРОИТЕЛЬНЫЕ РЕШЕНИЯ"
        individual_services = []
        # Первая услуга из каждой категории для карточек
        first_services_list = []
        for category in categories:
            first_service = category.services.filter(is_active=True).order_by('order').first()
            if first_service:
                individual_services.append(first_service)
                first_services_list.append(first_service)
            else:
                first_services_list.append(None)
        context['individual_services'] = individual_services
        context['first_services_list'] = first_services_list  # В том же порядке, что и categories
        
        # Рекомендуемые проекты (отключено)
        # context['featured_projects'] = Project.objects.filter(
        #     is_active=True, 
        #     is_featured=True
        # )[:6]
        context['featured_projects'] = []
        
        # Клиенты
        context['clients'] = Client.objects.filter(is_active=True)[:12]
        
        # Лицензии
        context['licenses'] = License.objects.filter(is_active=True)[:8]
        
        # Сертификаты для главной страницы
        context['certificates'] = Certificate.objects.filter(is_active=True).order_by('order')[:6]
        
        # Только первая услуга для секции "Наши услуги" на главной
        context['first_home_service'] = HomeService.objects.filter(is_active=True).order_by('order').first()
        
        # Изображения проектов для секции "ИНДИВИДУАЛЬНЫЕ СТРОИТЕЛЬНЫЕ РЕШЕНИЯ" (первые 4)
        # Используем изображения из ServiceImage, которые уже есть в админке
        context['home_project_images'] = ServiceImage.objects.filter(is_active=True).order_by('order')[:4]
        
        # Изображения для секции "КТО МЫ" (первые 4)
        context['who_we_are_images'] = WhoWeAreImage.objects.filter(is_active=True).order_by('order')[:4]
        
        return context


class AboutView(TemplateView):
    """Страница о компании"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            context['company'] = CompanyInfo.objects.filter(is_active=True).first()
        except CompanyInfo.DoesNotExist:
            context['company'] = None
        
        # Ключевые цифры
        context['key_figures'] = KeyFigure.objects.filter(is_active=True)
        
        # Сертификаты (последние 4)
        context['recent_certificates'] = Certificate.objects.filter(is_active=True)[:4]
        
        # Лицензии (последние 4)
        context['recent_licenses'] = License.objects.filter(is_active=True)[:4]
        
        return context


class CertificatesView(ListView):
    """Страница сертификатов"""
    model = Certificate
    template_name = 'core/certificates.html'
    context_object_name = 'certificates'
    paginate_by = 12
    
    def get_queryset(self):
        return Certificate.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Сертификаты'
        return context


class LicensesView(ListView):
    """Страница лицензий"""
    model = License
    template_name = 'core/licenses.html'
    context_object_name = 'licenses'
    paginate_by = 12
    
    def get_queryset(self):
        return License.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Лицензии'
        return context


class AllServicesView(ListView):
    """Страница со всеми услугами из HomeService"""
    model = HomeService
    template_name = 'core/all_services.html'
    context_object_name = 'services'
    paginate_by = None
    
    def get_queryset(self):
        return HomeService.objects.filter(is_active=True).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Наши услуги'
        return context
