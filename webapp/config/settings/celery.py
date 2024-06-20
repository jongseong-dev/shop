import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
app = Celery("config")  # 애플리케이션 인스턴스 생성

# 커스텀 구성으로 로드한다. namespace 속성은 settings.py 파일에 Celery 관련 설정이 가질 접두사를 지정한다.
# 예: CELERY_BROKER_URL
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()  # 각 애플리케이션 디렉터리에서 tasks.py 파일을 찾아 로드한다.
