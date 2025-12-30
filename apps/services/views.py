from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service, ServiceCategory


class ServiceListView(ListView):
    """Список всех услуг"""
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = None  # Убираем пагинацию для единой страницы
    
    def get_queryset(self):
        # Получаем все активные услуги, отсортированные по порядку
        return Service.objects.filter(is_active=True).select_related('category').order_by('category__order', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order')
        context['page_title'] = 'Услуги'
        return context


class ServiceCategoryView(DetailView):
    """Услуги по категории"""
    model = ServiceCategory
    template_name = 'services/category_detail.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        return ServiceCategory.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.object.services.filter(is_active=True).order_by('order')
        context['page_title'] = self.object.name
        return context


class ServiceDetailView(DetailView):
    """Детальная страница услуги"""
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:3]
        # context['related_projects'] = self.object.projects.filter(is_active=True)[:6]  # Портфолио отключено
        return context
