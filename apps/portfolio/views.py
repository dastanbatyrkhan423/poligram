from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Project, ProjectCategory


class ProjectListView(ListView):
    """Список проектов портфолио"""
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Project.objects.filter(is_active=True).select_related('client').prefetch_related('services', 'categories')
        
        # Фильтр по категории
        category = self.request.GET.get('category')
        if category and category != 'all':
            queryset = queryset.filter(categories__slug=category)
        
        # Фильтр по году
        year = self.request.GET.get('year')
        if year and year != 'all':
            queryset = queryset.filter(year=year)
        
        # Фильтр по услуге
        service = self.request.GET.get('service')
        if service and service != 'all':
            queryset = queryset.filter(services__slug=service)
        
        return queryset.distinct().order_by('-year', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.filter(is_active=True)
        context['years'] = Project.objects.filter(is_active=True).values_list('year', flat=True).distinct().order_by('-year')
        context['page_title'] = 'Портфолио'
        
        # Текущие фильтры
        context['current_category'] = self.request.GET.get('category', 'all')
        context['current_year'] = self.request.GET.get('year', 'all')
        context['current_service'] = self.request.GET.get('service', 'all')
        
        return context


class ProjectDetailView(DetailView):
    """Детальная страница проекта"""
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(is_active=True).select_related('client').prefetch_related('images', 'services', 'categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Другие проекты клиента
        context['client_projects'] = Project.objects.filter(
            client=self.object.client,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        
        # Похожие проекты (по услугам)
        related_projects = Project.objects.filter(
            services__in=self.object.services.all(),
            is_active=True
        ).exclude(id=self.object.id).distinct()[:4]
        context['related_projects'] = related_projects
        
        return context
