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
2. stripe checkout 통합하기
    - payment_process: stripe 결제 세션을 생성하고 클라이언트를 Stirpe에서 호스팅하는 결제 폼으로 리디렉션 한다.
    - payment_completed: 결제 성공 메시지를 표시
    - payment_canceled: 결제 취소 메시지를 표시

### 결제 처리 흐름

1. 주문이 생성되면 사용자는 `payment_process`뷰로 리디렉션 된다. 주문 요약과 결제를 진행할 수 있는 버튼이 사용자에게 표시된다.
2. 사용자가 결제를 진행하면 Stripe 결제 세션이 생성된다.    
결제 세션에는 사용자가 구매할 항목의 목록, 결제 성공 후 사용자를 리디렉션할 URL, 결제가 취소된 경우 사용자를 리디렉션할 URL이 포함된다.
3. 이 보기는 사용자를 Stripe 호스팅 결제 페이지로 리디렉션한다. 이 페이지에는 결제폼이 포함된다. 고객이 신용카드 세부 정보를 입력하고 폼을 제출한다.
4. Stripe에서 결제를 처리하고 클라이언트를 payment_completed 뷰로 리디렉션 한다.   
고객이 결제를 완료하지 않으면 Stripe는 대신 고객을 pament_canceled 뷰로 리디렉션 한다.