# 목차

<!-- TOC -->
* [목차](#목차)
* [프로젝트의 기능 소개](#프로젝트의-기능-소개)
  * [목표](#목표)
  * [기능](#기능-)
    * [쇼핑 카트](#쇼핑-카트)
    * [고객 주문](#고객-주문)
    * [비동기](#비동기)
    * [결제주문](#결제주문)
    * [주문을 CSV 파일로 내보내기](#주문을-csv-파일로-내보내기)
    * [커스텀 뷰로 관리자 사이트 확장하기](#커스텀-뷰로-관리자-사이트-확장하기)
    * [동적으로 PDF 인보이스 생성하기](#동적으로-pdf-인보이스-생성하기)
    * [쿠폰 시스템](#쿠폰-시스템)
    * [추천 엔진 구축하기](#추천-엔진-구축하기)
* [프로젝트 시작하기](#프로젝트-시작하기)
  * [필요한 요소 세팅 및 Django App 실행하기](#필요한-요소-세팅-및-django-app-실행하기)
    * [1. 패키지 설치](#1-패키지-설치)
    * [2. DB 설치 후 migration](#2-db-설치-후-migration)
    * [3. Django 실행하기](#3-django-실행하기)
    * [4. Django test 실행하기](#4-django-test-실행하기)
  * [번외. docker-compose로 실행하기](#번외-docker-compose로-실행하기)
    * [1. docker-compose 서비스 실행](#1-docker-compose-서비스-실행)
    * [2. docker-compose 서비스 종료](#2-docker-compose-서비스-종료)
  * [환경변수](#환경변수)
    * [Django Config](#django-config)
    * [DB](#db)
    * [EMAIL](#email)
<!-- TOC -->

# 프로젝트의 기능 소개

- 온라인 상점(Shop)
  - "예제로 배우는 Django 4" 책을 보고 만든 예제 Repo

## 목표
- 전자 상거래 플랫폼의 필수 기능을 구축하고자 한다.
- 온라인 상점에서 고객은 제품을 조회하여 장바구니에 추가할 수 있다.
- 할인 코드를 적용하고 결제 프로세스를 거쳐 신용카드로 결제한 뒤 송장을 받을 수 있다.
- 고객에게 제품을 추천하는 추천 엔진을 구현하고 국제화를 사용해 여러 언어로 사이트를 제공한다.

## 기능 

### [쇼핑 카트](docs/shopping_cart.md)
### [고객 주문](docs/order.md)
### [비동기](docs/async.md)
### [결제주문](docs/payment.md)
### [주문을 CSV 파일로 내보내기](docs/csv.md)
### [커스텀 뷰로 관리자 사이트 확장하기](docs/custom_view.md)
### [동적으로 PDF 인보이스 생성하기](docs/pdf_invoice.md)
### [쿠폰 시스템](docs/coupon.md)
### [추천 엔진 구축하기](docs/recommend.md)

----
# 프로젝트 시작하기

## 필요한 요소 세팅 및 Django App 실행하기

- 들어가기에 앞서 `poetry`와 `docker`를 설치해주세요.
    - poetry 설치 방법: https://python-poetry.org/docs/#installation
    - docker 설치 방법: https://docs.docker.com/engine/install/

- DJANGO_SETTING_MODULE 설정하기
    - 현재 개발환경에서는 `config.settings.local`을 사용하고 있습니다.
    - 따라서 명령마다 --settings 옵션을 넣기 불편하다면 **DJANGO_SETTING_MODULE**을 `config.settings.local`로 환경변수로 설정해주세요.

### 1. 패키지 설치

- poetry를 통해 패키지를 설치합니다.

  ```bash
  poetry install
  ```

- 가상환경이 활성화 되었다면 `pre-commit`을 설치합니다.

  ```bash
  pre-commit install
  ```

### 2. DB 설치 후 migration

- django를 띄우기 위해 db를 설치합니다.
  ```bash
  docker-compose up -d db
  ```

- 해당 db가 무사히 실행되었다면, migration을 실행합니다.
- 이떄 주의할 점은 project 위치는 webapp 이므로 `webapp`으로 이동 후 실행합니다.
  ```bash 
  python manage.py migrate --settings=config.settings.local
  ```

### 3. Django 실행하기

- migration이 완료되었다면, django를 실행합니다.

  ```bash
  python manage.py runserver --settings=config.settings.local
  ```

### 4. Django test 실행하기

- test는 아래와 같이 실행합니다.

- Linux, MacOS
  ```bash
  pytest
  ```

- 만약 test 가 제대로 실행되지 않는다면 pytest의 실행 위치가 `webapp` 디렉토리인지 확인해주세요.

## 번외. docker-compose로 실행하기

- 만약 docker-compose를 통해 Django를 실행시키고 싶다면 steps를 따라주세요.

### 1. docker-compose 서비스 실행

- docker compose 를 통해 db와 test, was를 실행합니다.

  ```bash
  docker-compose up --build -d db
  docker-compose up --build web 
  docker-compose up --build test_web 
  ```

### 2. docker-compose 서비스 종료

- 확인했다면 docker-compose에 떠있는 container를 종료시킵니다.

  ```bash
  docker-compose down
  ```

## 환경변수

- 기본값이 없는 경우 **직접 지정해야 합니다.**

### Django Config

| 변수명                    | 기본값            | 비고                                                      |
|------------------------|----------------|---------------------------------------------------------| 
| DJANGO_SETTINGS_MODULE | 없음             |                                                         |
| SECRET_KEY             | 94n7fx27pd-... | local 환경과 test 환경에서는 기본값을 사용하지만 <br/> prod에서는 주입해야 합니다. |

### DB

| 변수명         | 기본값       |
|-------------|-----------|
| DB_NAME     | postgres  |
| DB_USER     | postgres  |
| DB_PASSWORD | postgres  |
| DB_HOST     | localhost |
| DB_PORT     | 5432      |

### EMAIL

| 변수명                 | 기본값                   |
|---------------------|-----------------------|
| EMAIL_HOST_PASSWORD | 없음                    |
| EMAIL_HOST          | smtp.gmail.com        |
| EMAIL_HOST_USER     | dlwhdtjd098@gmail.com |
| EMAIL_PORT          | 587                   |
| EMAIL_USE_TLS       | True                  |
