from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(
        db_comment="사용자가 구매 시 쿠폰을 적용하기 위해 입력해야 하는 코드"
    )
    valid_to = models.DateTimeField(db_comment="쿠폰 유효 기간의 시작 시점을 나태내는 날짜/시간 값")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage value (0 to 100)",
        db_comment="할인율을 나타내는 정수 값",
    )
    active = models.BooleanField(db_comment="쿠폰이 활성 상태인지를 나타내는 값")

    def __str__(self):
        return self.code
