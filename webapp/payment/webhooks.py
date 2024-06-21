import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order


@csrf_exempt  # 모든 POST 요청에 기본적으로 수행되는 CSRF 유효성 검사를 장고가 수행하지 못하도록 하는데 사용한다.
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # 잘못된 페이로드
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # 잘못된 서명
        return HttpResponse(status=400)
    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # 주문을 결제 완료로 표시
            order.paid = True
            order.save()
    return HttpResponse(status=200)
