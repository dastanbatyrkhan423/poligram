from django.core.management.base import BaseCommand
from apps.core.models import CompanyInfo, KeyFigure, Client
from apps.services.models import ServiceCategory, Service


class Command(BaseCommand):
    help = 'Create sample data for Poligram website'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Company info
        company, created = CompanyInfo.objects.get_or_create(
            name="ТОО «ПОЛИГРАМ»",
            defaults={
                'short_description': 'ТОО «ПОЛИГРАМ» выполняет полный комплекс строительно-монтажных, отделочных и инженерных работ 1 категории',
                'full_description': 'Компания на рынке 19 лет. ТОО «ПОЛИГРАМ» выполняет полный комплекс строительно-монтажных, отделочных и инженерных работ 1 категории.',
                'founded_year': 2006,
                'phone': '+7 (727) 345-67-89',
                'email': 'info@poligram.kz',
                'address_almaty': 'г. Алматы, ул. Примерная, 123',
                'working_hours': 'Пн-Пт: 09:00 - 18:00',
            }
        )

        # Key figures
        key_figures = [
            {'title': 'Проектов', 'value': '350+', 'description': 'Успешно реализованных проектов', 'icon': '🏗️', 'order': 1},
            {'title': 'Лет опыта', 'value': '19', 'description': 'На рынке строительных услуг', 'icon': '📅', 'order': 2},
            {'title': 'Категория лицензии', 'value': '1', 'description': 'Высшая категория допуска', 'icon': '📜', 'order': 3},
            {'title': 'ISO сертификата', 'value': '4', 'description': 'Международные стандарты качества', 'icon': '🏆', 'order': 4},
        ]

        for data in key_figures:
            KeyFigure.objects.get_or_create(title=data['title'], defaults=data)

        # Service categories
        categories = [
            {'name': 'Проектирование', 'slug': 'proektirovanie', 'icon': '📐', 'order': 1},
            {'name': 'Строительство', 'slug': 'stroitelstvo', 'icon': '🏗️', 'order': 2},
        ]

        for data in categories:
            ServiceCategory.objects.get_or_create(slug=data['slug'], defaults=data)

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('Website: http://127.0.0.1:8000/')
        self.stdout.write('Admin: http://127.0.0.1:8000/admin/ (admin / admin123)')
