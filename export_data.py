#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poligram_website.settings')
django.setup()

from django.core.management import call_command
from django.core.management.base import CommandError

if __name__ == '__main__':
    try:
        # Экспортируем данные с правильной кодировкой
        with open('data.json', 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                '--exclude', 'auth.permission',
                '--exclude', 'contenttypes',
                '--exclude', 'sessions',
                '--exclude', 'admin.logentry',
                '--indent', '2',
                stdout=f
            )
        print("SUCCESS: Data exported to data.json")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

