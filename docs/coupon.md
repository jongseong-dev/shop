# 쿠폰 시스템 만들기
- 온라인 쿠폰은 일반적으로 사용자에게 제공되는 코드로 구성되고 특정기간동안 유효하다.
- 쿠폰은 사용할 수 있는 횟수에 제한이 없으며 장바구니의 총금액에 적용된다.

## goal
- 쿠폰 시스템 생성하기
- 카트에 쿠폰 적용하기
- 주문에 쿠폰 적용하기
- 스트라이프 체크 아웃용 쿠폰 생성하기
- 일반적으로 함께 구매하는 제품 저장하기
- Redis로 제품 추천 엔진 구축하기

## 장바구니에 쿠폰 적용하기

### 쿠폰 적용하는 순서
1. 사용자가 카트에 제품을 추가한다.
2. 사용자가 카트 상세 페이지에 표시되는 폼에 쿠폰 코드를 입력한다.
3. 사용자가 쿠폰 코드를 입력하고 폼을 제출하면 해당 코드의 현재 유효한 기존 쿠폰을 찾는다.   
쿠폰 코드가 사용자가 입력한 코드와 일치하는지, active 속성이 True인지, 현재 날짜가 valid_from과 valid_to 값 사이에 있는지 확인한다.
4. 쿠폰이 발견되면 사용자 세션에 저장하고 쿠폰에 적용된 할인 금액과 반영된 총금액을 카트에 표시한다.
5. 사용자가 주문하면 해당 주문에 쿠폰을 저장한다.

## Stripe Checkout용 쿠폰 생성하기
- Stripe를 사용하여 할인 쿠폰을 정의하고 일회성 결제에 연결하도록 한다.

```python
...
if order.coupon:
    stripe_coupon = stripe.Coupon.create(
        name=order.coupon.code,
        percent_off=order.coupon.discount,
        duration="once",
    )
    session_data["discounts"] = [{"coupon": stripe_coupon.id}]

```
