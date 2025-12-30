from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap для статических страниц"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'core:home',
            'core:about', 
            'core:certificates',
            'core:licenses',
            'services:service_list',
            'portfolio:project_list',
            'contact:contact',
        ]
    
    def location(self, item):
        return reverse(item)
