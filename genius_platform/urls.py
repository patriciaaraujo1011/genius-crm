from django.contrib.auth import views as auth_views
from django.urls import path

from crm import views as crm_views
from crm.admin import admin_site

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", crm_views.dashboard, name="dashboard"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login_direct",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("contacts/", crm_views.contacts, name="contacts"),
    path("products/", crm_views.products, name="products"),
    path("orders/", crm_views.orders, name="orders"),
    path("funnels/", crm_views.funnels, name="funnels"),
    path(
        "funnels/templates/",
        crm_views.funnel_templates,
        name="funnel_templates",
    ),
    path(
        "funnels/<slug:slug>/", crm_views.funnel_detail, name="funnel_detail"
    ),
    path("courses/", crm_views.courses, name="courses"),
    path(
        "courses/<slug:slug>/", crm_views.course_detail, name="course_detail"
    ),
    path("pipeline/", crm_views.pipeline_list, name="pipeline_list"),
    path(
        "pipeline/<int:pipeline_id>/",
        crm_views.pipeline_board,
        name="pipeline_board",
    ),
    path("broadcast/", crm_views.broadcast, name="broadcast"),
    path("sequences/", crm_views.sequences, name="sequences"),
    path("opt-in/", crm_views.optin_page, name="optin_page"),
    path("opt-in/thank-you/", crm_views.optin_thankyou, name="optin_thankyou"),
    path("opt-in/<slug:slug>/", crm_views.optin_page, name="optin_page_slug"),
    path("api/contacts/", crm_views.api_add_contact, name="api_add_contact"),
    path("api/orders/", crm_views.api_create_order, name="api_create_order"),
    path(
        "api/broadcast/",
        crm_views.api_send_broadcast,
        name="api_send_broadcast",
    ),
    path(
        "api/pipeline/",
        crm_views.api_create_pipeline,
        name="api_create_pipeline",
    ),
    path(
        "api/opportunity/",
        crm_views.api_create_opportunity,
        name="api_create_opportunity",
    ),
    path(
        "api/opportunity/stage/",
        crm_views.api_update_opportunity_stage,
        name="api_update_opportunity_stage",
    ),
    path(
        "api/webhook/stripe/", crm_views.stripe_webhook, name="stripe_webhook"
    ),
    path("offer-expired/", crm_views.offer_expired, name="offer_expired"),
    path(
        "funnel/<slug:slug>/", crm_views.funnel_landing, name="funnel_landing"
    ),
    path(
        "funnel/<slug:slug>/order/",
        crm_views.funnel_order,
        name="funnel_order",
    ),
    path(
        "funnel/<slug:slug>/checkout/",
        crm_views.funnel_checkout,
        name="funnel_checkout",
    ),
    path(
        "funnel/<slug:slug>/thank-you/",
        crm_views.funnel_thankyou,
        name="funnel_thankyou",
    ),
    path(
        "funnel/<slug:slug>/upsell/",
        crm_views.funnel_upsell,
        name="funnel_upsell",
    ),
]
