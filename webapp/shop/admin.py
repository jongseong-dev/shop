from django.contrib import admin

from shop.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {
        "slug": ("name",)
    }  # 다른 필드의 값을 사용해서 값이 자동으로 설정되는 필드 설정


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "available", "created", "updated"]
    list_filter = ["available", "created", "updated"]
    list_editable = [
        "price",
        "available",
    ]  # 목록에서 해당 속성을 수정할 수 있음
    prepopulated_fields = {"slug": ("name",)}
