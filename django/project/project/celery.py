from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env (если он используется)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Установка путей для GDAL и GEOS
os.environ.setdefault(
    "GDAL_LIBRARY_PATH",
    os.getenv(
        "GDAL_LIBRARY_PATH",
        r"C:\Users\aleksandrs.sloka\Desktop\vs_codes\vue_js\django\env\Lib\site-packages\osgeo\gdal303.dll"
    )
)

os.environ.setdefault(
    "GEOS_LIBRARY_PATH",
    os.getenv(
        "GEOS_LIBRARY_PATH",
        r"C:\Users\aleksandrs.sloka\Desktop\vs_codes\vue_js\django\env\Lib\site-packages\osgeo\geos_c.dll"
    )
)

# Настройка Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Настройки для отладки (1 поток и использование solo pool)
app.conf.worker_concurrency = 1
app.conf.pool = 'solo'

# Загрузка конфигурации Celery из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
