# 결제하기
- 사용자가 신용카드로 결제할 수 있도록 결제 게이트웨이를 사이트에 통합하는 방법을 알아보자

## Goal
- 프로젝트에 stripe 결제 게이트웨이 통합하기
- Stripe로 신용카드 결제 처리하기
- 결제 알림 처리하기
- 주문을 CSV 파일로 내보내기
- 관리 사이트에 대한 커스텀 뷰 마늘기
- 동적으로 PDF 인보이스 생성하기

## 전자결제 게이트웨이 통합하기
- 결제 게이트웨이인 Stripe를 사용하여 결제를 처리하는 방법을 알아보자


### Stripe 계정 만들기
- [Stripe](https://stripe.com)에 가입하고 계정을 만든다

### Stripe 세팅하기

- 설치
```bash
pip install stripe
```

- settings.py에 stripe api key 추가
```python
# settings.py
import os


STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
```

### 결제 프로세스 구축하기

1. 앱 생성
2. 