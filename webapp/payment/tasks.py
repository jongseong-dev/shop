from celery import shared_task
from django.core.mail import EmailMessage

from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f"My Shop - Invoice no. {order.id}"
    message = "Please, find attached the invoice for your recent purchase."
    email = EmailMessage(
        subject, message, "dlwhdtjd098@gmail.com", [order.email]
    )
    email.send()
