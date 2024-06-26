from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from coupons.models import Coupon


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,  # 대소문자를 구분하지 않고 정확히 일치하는 필드값 조회
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
    return redirect("cart:cart_detail")
