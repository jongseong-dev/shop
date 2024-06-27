# Generated by Django 4.2.13 on 2024-06-27 02:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("coupons", "0001_initial"),
        ("orders", "0002_order_stripe_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="coupons.coupon",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="discount",
            field=models.IntegerField(
                default=0,
                help_text="쿠폰 할인 금액",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
    ]