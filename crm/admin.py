from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.shortcuts import render
from django.urls import path

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


def funnel_templates_view(request):
    templates = [
        {
            "name": "Sales Template 1",
            "file": "sales_template_1.html",
            "description": "Landing/sales page with hero, video, testimonials, pricing, FAQ",
        },
        {
            "name": "Order Template 1",
            "file": "order_template_1.html",
            "description": "Checkout page with order form, order bumps, product summary",
        },
        {
            "name": "Upsell Template 1",
            "file": "upsell_template_1.html",
            "description": "Post-purchase upsell with urgency, value stack, comparison",
        },
        {
            "name": "Thank You Template 1",
            "file": "thank_you_template_1.html",
            "description": "Confirmation page with access instructions and next steps",
        },
    ]
    context = {
        "title": "Funnel Templates",
        "templates": templates,
        "app_label": "crm",
    }
    return render(request, "admin/funnel_templates.html", context)


class MyAdminSite(AdminSite):
    site_header = "Genius CRM"
    site_title = "Genius CRM Admin"
    index_title = "Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "funnel-templates/",
                self.admin_view(funnel_templates_view),
                name="funnel_templates",
            ),
        ]
        return my_urls + urls

    def get_menu(self, request):
        menu = super().get_menu(request)
        menu.add_break()
        return menu


admin_site = MyAdminSite(name="myadmin")


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


admin_site.register(
    [MemberProgress, GamificationPoints, UserBadge, EmailSequenceStep]
)

admin_site.register(Contact)
admin_site.register(Product)
admin_site.register(Order)
admin_site.register(Funnel)
admin_site.register(FunnelPage)
admin_site.register(Module)
admin_site.register(Lesson)
admin_site.register(Broadcast)
admin_site.register(EmailSequence)
admin_site.register(Badge)
