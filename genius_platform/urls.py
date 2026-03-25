from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from crm import views as crm_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', crm_views.dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login_direct'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contacts/', crm_views.contacts, name='contacts'),
    path('products/', crm_views.products, name='products'),
    path('orders/', crm_views.orders, name='orders'),
    path('funnels/', crm_views.funnels, name='funnels'),
    path('funnels/<slug:slug>/', crm_views.funnel_detail, name='funnel_detail'),
    path('courses/', crm_views.courses, name='courses'),
    path('courses/<slug:slug>/', crm_views.course_detail, name='course_detail'),
    path('pipeline/', crm_views.pipeline_list, name='pipeline_list'),
    path('pipeline/<int:pipeline_id>/', crm_views.pipeline_board, name='pipeline_board'),
    path('broadcast/', crm_views.broadcast, name='broadcast'),
    path('sequences/', crm_views.sequences, name='sequences'),
    path('opt-in/', crm_views.optin_page, name='optin_page'),
    path('opt-in/<slug:slug>/', crm_views.optin_page, name='optin_page_slug'),
    path('opt-in/thank-you/', crm_views.optin_thankyou, name='optin_thankyou'),
    path('api/contacts/', crm_views.api_add_contact, name='api_add_contact'),
    path('api/orders/', crm_views.api_create_order, name='api_create_order'),
    path('api/broadcast/', crm_views.api_send_broadcast, name='api_send_broadcast'),
    path('api/pipeline/', crm_views.api_create_pipeline, name='api_create_pipeline'),
    path('api/opportunity/', crm_views.api_create_opportunity, name='api_create_opportunity'),
    path('api/opportunity/stage/', crm_views.api_update_opportunity_stage, name='api_update_opportunity_stage'),
]
