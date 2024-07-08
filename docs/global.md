# 국제화하기

## 목표
- 번역 파일 관리하기
- 파이썬 코드 번역하기
- 템플릿 번역하기
- Rosetta를 사용하여 번역 관리하기
- URL 패턴 번역 및 URL에 언어 접두사 사용하기
- 사용자가 언어를 전환할 수 있도록 허용하기
- django-parler를 사용해서 모델 번역하기
- ORM에서 번역 사용하기
- 번역을 사용하도록 뷰 조정하기
- django-localflavor의 지역화된 폼 필드 사용하기

## 장고로 국제화하기

- 장고는 완전한 국제화 및 지역화 지원을 제공한다.
- 애플리케이션을 여러 언어로 번역할 수 있으며 날짜, 시간, 숫자 및 시간대의 지역별 서식을 처리한다.
- 국제화와 지역화의 차이점
    - 국제화(약칭으로 i18n)는 소프트웨어가 특정 언어나 지역에 고정되지 않도록 다양한 언어 및 지역에서의 잠재적인 사용에 맞도록 조정하는 프로세스이다.
    - 지역화(약칭으로 l10n)는 소프트웨어를 실제로 번역해서 특정 로케일에 맞게 조정하는 프로세스이다.
- 메시지 파일을 생성하고 관리하기 위해 GNU gettext 툴셋을 사용한다.

## 국제화 및 지역화 설정
- USE_I18N: 장고의 번역 시스테 활성화 여부를 지정하는 bool. 기본값은 True
- USE_L10N: 지역화된 서식 지정의 활성화 여부를 나타내는 bool. 활성화되면 날짜 및 숫자에 지역화된 서식이 사용된다. 기본값은 False
- USE_TZ: 날짜/시간을 표준 시간대로 인식할지를 지정하는 bool. startproject 명령으로 프로젝트를 만들면 True로 설정
- LANGUAGE_CODE: 프로젝트의 기본 언어 코드. 이 설정을 적용하려면 USE_I18N을 True로 설정해야 한다.
- LANGUAGES: 프로젝트에 사용 가능한 언어가 포함된 tuple. 언어 코드와 언어 이름의 두 가지 튜플로 구성된다.
- LOCALE_PATHS: 장고가 프로젝트의 번역이 포함된 메시지 파일을 찾는 디렉터리 목록
- TIME_ZONE: 프로젝트의 기본 시간대. 새 프로젝트를 만들 때 'UTC'로 설정된다.

### 국제화 관리 명령
- 장고에는 번역을 관리하기 위한 다음과 같은 관리 명령이 포함되어 있다.
  - makemessages: 이 명령은 소스 트리를 실행하여 번역용으로 표시된 모든 문자열을 찾고 locale 디렉터리에 .po 메시지 파일을 생성하거나 업데이트 한다. 각 언어마다 단일 .po 파일이 생서된다.
  - compilemessages: 기존 .po 메시지 파일을 번역을 검색하는 데 사용되는 .mo 파일로 컴파일 한다.

### gettext 툴킷 설치하기
- macOS: `brew install gettext` or `brew link --force gettext`(강제로 링크하기)
- windows: [django 문서 참조](https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#gettext-on-windows)

### 장고가 현재 언어를 결정하는 방법
- 장고에는 요청 데이터를 기반으로 현재 언어를 결정하는 미들웨어가 함께 제공된다.
- 이 미들웨어는 `django.middleware.locale.LocaleMiddleware`이다.
- 해당 미들웨어는 다음과 같은 작업을 한다.
  1. i18n_patterns를 사용하는 경우, 다시 말해 번역된 URL 패턴을 사용하는 경우에는 요청된 URL에서 언어 접두사를 찾아 현재 언어를 결정한다.
  2. 언어 접두사를 찾을 수 없으면 현재 사용자의 세션에서 기존 `LANGUAGE_SESSION_KEY`를 찾는다.
  3. 세션에 언어가 설정되어 있지 않은 경우, 현재 언어를 나타내는 쿠키를 찾는다 이 쿠키의 이름은 `LANGUAGE_COOKIE_NAME` 설정에서 제공할 수 있다. 기본적으로 이 쿠키의 이름은 `django_language`이다.
  4. 이 쿠키를 찾을 수 없으면 요청의 `Accept-Language` HTTP 헤더를 찾는다.
  5. Accept-Language 헤더에 언어가 지정되지 않은 경우, 장고는 `LANGUAGE_CODE` 설정에 정의된 언어를 사용한다.
- 기본적으로 장고는 `LocaleMiddleware`를 사용하지 않는 한 `LANGUAGE_CODE` 설정에 정의된 언어를 사용 한다. 
- 여기에 설명된 프로세스는 `LocaleMiddleware`를 사용할 때만 적용된다. 

## 국제화를 위한 준비하기

```python
# settings.py

LANGUAGES = [
  ("en", "English"),
  ("ko", "Korean"),
]

```