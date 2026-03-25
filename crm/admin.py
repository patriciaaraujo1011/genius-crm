from django.contrib import admin

from .models import (
    Badge,
    Broadcast,
    Contact,
    EmailSequence,
    EmailSequenceStep,
    Funnel,
    FunnelPage,
    GamificationPoints,
    Lesson,
    MemberProgress,
    Module,
    Order,
    OrderBump,
    Product,
    UserBadge,
)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "source",
        "is_buyer",
        "created_at",
    ]
    list_filter = ["source", "is_buyer"]
    search_fields = ["email", "first_name", "last_name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "product_type", "is_active", "created_at"]
    list_filter = ["product_type", "is_active"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["contact", "product", "amount", "status", "created_at"]
    list_filter = ["status", "product"]
    search_fields = ["contact__email", "stripe_payment_id"]


class FunnelPageInline(admin.TabularInline):
    model = FunnelPage
    extra = 1
    ordering = ["order"]


class OrderBumpInline(admin.TabularInline):
    model = OrderBump
    extra = 1
    ordering = ["order"]


@admin.register(Funnel)
class FunnelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "is_active",
        "offer_end_date",
        "created_at",
    ]
    list_filter = ["is_active"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [FunnelPageInline, OrderBumpInline]


@admin.register(FunnelPage)
class FunnelPageAdmin(admin.ModelAdmin):
    list_display = ["funnel", "page_type", "title", "order"]
    list_filter = ["page_type", "funnel"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["title", "product", "order"]
    list_filter = ["product"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "module",
        "content_type",
        "order",
        "duration_minutes",
    ]
    list_filter = ["content_type", "module__product"]


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ["subject", "segment", "sent_at", "open_rate"]
    list_filter = ["segment"]


@admin.register(EmailSequence)
class EmailSequenceAdmin(admin.ModelAdmin):
    list_display = ["name", "trigger", "created_at"]
    prepopulated_fields: dict = {}


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ["name", "points_required"]


admin.site.register(
    [MemberProgress, GamificationPoints, UserBadge, EmailSequenceStep]
)
