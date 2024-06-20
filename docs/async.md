# 비동기 작업
- 순서대로 작업을 진행하는 동기 작업과는 달리 비동기 작업은 작업의 제어권을 다른 곳에 넘겨주고 결과를 기다리지 않고 다음 작업을 수행할 수 있다.
- 일부 작업을 백그라운드에서 실행함으로써 애플리케이션의 성능을 향상시킬 수 있다.

## 워커, 메시지 큐 및 메시지 브로커

### 워커
- 웹 서버가 요청을 처리하고 응답을 반환하는 동안 비동기 작업을 처리하려면 워커(Worker)라는 이름의 또 다른 작업 기반 서버가 필요하다.

### 메시지 큐, 메시지 브로커
- 워커에게 어떤 작업을 실행할지 알려주려면 메시지를 보내야 한다.
- 워커는 메시지 큐(Message Queue)나 메시지 브로커(Message Broker)를 통해 메시지를 받아 작업을 실행한다.
- 메시지 큐를 관리하기 위해서 메시지 브로커가 필요하다.
- 메시지 브로커는 메시지를 공식 메시징 프로토콜로 변환하고 여러 수신자의 메시지 큐를 관리하는데 사용한다.
- 메시지 브로커는 메시지의 안정적인 저장과 메시지 전달을 보장한다.
- 메시지 브로커를 사용하면 메시지 큐를 만들고, 메시지를 라우팅하고, 작업자 간에 메시지를 배포하는 등의 작업을 수행할 수 있다.

### Celery 및 RabbitMQ 사용하기
- Celery는 방대한 양의 메시지를 처리할 수 있는 분산 작업 큐이다.
- 새로운 메시지를 가져와 비동기 작업을 처리하기 위해 메시지 브로커를 청취해서 새로운 메시지를 가져오는 Celery 워커를 실행해보자.
- Celery는 특정 시간에 작업을 실행하도록 하는 Scheduler도 제공한다.
- 메시지 브로커로는 `RabbitMQ`를 사용해보자
- RabbitMQ는 AMQP(Advanced Message Queuing Protocol)를 구현한 오픈 소스 메시지 브로커이다.

## 세팅하기

### RabbitMQ

- docker로 실행하기
```bash
docker run -dit --name rabbitmq \
       -e RABBITMQ_DEFAULT_USER=user \   # docker default user를 guest 대신 설정하기
       -e RABBITMQ_DEFAULT_PASS=<password> \
       -p 5672:5672 \
       -p 15672:15672 \
       rabbitmq:3-management
```

### Celery
- 라이브러리 설치
```bash
pip install celery
```

1. celery 기본 환경 설정하기
```python
# settings.py와 같은 레벨에 celery.py을 만들어서 해당 설정 추가

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
app = Celery("config")  # 애플리케이션 인스턴스 생성

# 커스텀 구성으로 로드한다. namespace 속성은 settings.py 파일에 Celery 관련 설정이 가질 접두사를 지정한다.
# 예: CELERY_BROKER_URL
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()  # 각 애플리케이션 디렉터리에서 tasks.py 파일을 찾아 로드한다.
```

2. settings.py __init__.py 에 Celery load 되는 설정하기
```python

from config.settings.celery import app as celery_app

__all__ = ["celery_app"]
```

3. celery 실행하기 
```bash
celery -A config worker -l info 
```


