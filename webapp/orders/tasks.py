from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def order_created(order_id):
    """
    주문이 성공적으로 생성될 때
    이메일 알림을 보내는 작업을 생성
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = (
        f"Dear {order.first_name},\n\n"
        f"You have successfully placed an order."
        f"Your order ID is {order.id}."
    )
    mail_sent = send_mail(
        subject, message, "dlwhdtjd098@gmail.com", [order.email]
    )
    return mail_sent
