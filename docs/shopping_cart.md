# 쇼핑 카트

## 목표

- 사용자가 구매하려는 제품을 선택할 수 있도록 쇼핑 카트를 만든다
- 최종 주문이 이루어질 때까지 제품을 선택하고 주문할 금액을 설정한 정보를 임시로 저장할 수 있다.
    - 사용자가 방문하는 동안 카트 항목이 유지되도록 카트는 세션에서 유지되어야 한다.
- 장고 세션 프레임워크를 사용하여 카트를 유지한다.

## 장고 세션 사용하기

### 개요
- 장고는 익명 세션과 사용자 세션을 지원하는 세션 프레임워크를 제공한다.
- 세션 프레임워크를 사용하여 각 방문자의 데이터를 저장하자.
    ```text
    세션 데이터는 서버 측에 저장되며, 쿠키 기반 세션 엔진을 사용하지 않는 한 쿠키에는 세션 ID를 담는다.
    세션 미들웨어는 쿠키의 송수신을 관리한다.
    ```
- 예시
```python
request.session["foo"] = "bar"  # 변수 설정
request.session.get("foo")      # 조회
del request.session["foo"]      # 삭제
```

- `NOTE`
  - 사용자가 사이트에 로그인하면 익명 세션이 사리지고 인증된 사용자를 위한 새로운 세션이 생성된다.
  - 사용자가 로그인 후에도 유지해야 하는 항목을 익명 세션에 저장한 경우에는 이전 세션의 데이터를 새로운 세션으로 복사해야 한다.
  - 이 작업은 장고 인증 시스템의 login() 함수를 사용해서 사용자를 로그인 시키기 전에 세션 데이터를 조회한 뒤 세션에 저장하면 된다.
```python
def login(request):
    if request.method == 'POST':
        # 로그인 로직 처리
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # 익명 세션에서 데이터 가져와서 로그인 사용자 세션에 저장하기
            anonymous_cart = request.session.get('anonymous_cart', None)
            if anonymous_cart:
                request.session['cart'] = anonymous_cart
                del request.session['anonymous_cart']
            
            return redirect('home')
        else:
            # 로그인 실패 처리
            pass
    else:
        # GET 요청 처리
        pass
```

### 세션 설정

- `SESSION_ENGIN`을 사용하면 세션이 저장되는 위치를 설정할 수 있다.
- 기본적으로 장고는 `django.contrib.sessions.backends.db`를 사용한다.
- 장고는 세션 데이터 저장을 위해 다음과 같은 옵션을 제공한다.
  - 데이터베이스 세션: 세션 데이터베이스에 저장 된다. 기본 세션 엔진이다
  - 파일 기반 세션: 세션 데이터가 파일 시스템에 저장된다.
  - 캐시 기반 세션: 세션 데이터는 캐시 백엔드에 저장 된다.
  - 캐시 데이터베이스 세션: 세션 데이터는 쓰기 전용 케시와 데이터베이스에 저장된다. 데이터가 아직 캐시에 없는 경우에만 데이터베이스에서 읽는다.
  - 쿠키 기반 세션: 세션 데이터는 브라우저로 전송되는 쿠키에 저장된다.
- 옵션
- `SESSION_COOKIE_AGE`: 세션 쿠키의 만료 시간을 설정한다. 기본값은 1209600(2주)이다.
- `SESSION_COOKIE_DOMAIN`: 세션 쿠키의 도메인을 설정한다. 크로스 도메인 쿠키를 사용하려면 `mydomain.com`으로 설정하고, 표준 도메인 쿠키를 사용하려면 `None`으로 설정한다.
- `SESSION_COOKIE_HTTPONLY`: 기본값인 `True`로 설정하면 세션 쿠키가 JavaScript에서 액세스 할 수 없다.
- `SESSION_COOKIE_SECURE`: HTTPS 연결인 경우에만 쿠키를 전송해야 함을 나타낸다. 기본값은 `False`이다.
- `SESSION_EXPIRE_AT_BROWSER_CLOSE`: 브라우저를 닫을 때 세션 쿠키를 삭제할지 여부를 나타낸다. 기본값은 `False`이다.
- `SESSION_SAVE_EVERY_REQUEST`: `True`인 경우 요청할 때마다 세션을 데이터베이스에 저장하는 부울 값이다. 세션이 저장될 때마다 만료시점도 업데이트 된다. 기본값은 `False`이다.