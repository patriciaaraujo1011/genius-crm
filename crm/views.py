from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Sum, Count
from .models import (
    Contact, Product, Order, Funnel, FunnelPage,
    Module, Lesson, MemberProgress, GamificationPoints,
    Badge, UserBadge, Broadcast, EmailSequence, EmailSequenceStep
)
import json


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


@login_required
def dashboard(request):
    total_contacts = Contact.objects.count()
    buyer_contacts = Contact.objects.filter(is_buyer=True).count()
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='completed').count()
    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    total_products = Product.objects.count()
    active_funnels = Funnel.objects.filter(is_active=True).count()
    total_broadcasts = Broadcast.objects.count()
    
    recent_contacts = Contact.objects.order_by('-created_at')[:5]
    recent_orders = Order.objects.select_related('contact', 'product').order_by('-created_at')[:5]
    top_products = Product.objects.annotate(order_count=Count('order')).order_by('-order_count')[:5]
    
    context = {
        'total_contacts': total_contacts,
        'buyer_contacts': buyer_contacts,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'active_funnels': active_funnels,
        'total_broadcasts': total_broadcasts,
        'recent_contacts': recent_contacts,
        'recent_orders': recent_orders,
        'top_products': top_products,
    }
    return render(request, 'dashboard.html', context)


@login_required
def contacts(request):
    contacts = Contact.objects.order_by('-created_at')
    return render(request, 'contacts.html', {'contacts': contacts})


@login_required
def products(request):
    products = Product.objects.order_by('-created_at')
    return render(request, 'products.html', {'products': products})


@login_required
def orders(request):
    orders = Order.objects.select_related('contact', 'product').order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})


@login_required
def funnels(request):
    funnels = Funnel.objects.prefetch_related('funnelpage_set').order_by('-created_at')
    return render(request, 'funnels.html', {'funnels': funnels})


@login_required
def funnel_detail(request, slug):
    funnel = Funnel.objects.prefetch_related('funnelpage_set').get(slug=slug)
    pages = funnel.funnelpage_set.all()
    return render(request, 'funnel_detail.html', {'funnel': funnel, 'pages': pages})


@login_required
def courses(request):
    products = Product.objects.filter(product_type='course')
    return render(request, 'courses.html', {'products': products})


@login_required
def course_detail(request, slug):
    product = Product.objects.prefetch_related('modules__lessons').get(slug=slug)
    return render(request, 'course_detail.html', {'product': product})


@login_required
def broadcast(request):
    broadcasts = Broadcast.objects.order_by('-sent_at')[:20]
    return render(request, 'broadcast.html', {'broadcasts': broadcasts})


@login_required
def sequences(request):
    sequences = EmailSequence.objects.prefetch_related('steps').all()
    return render(request, 'sequences.html', {'sequences': sequences})


@require_http_methods(["POST"])
def api_add_contact(request):
    try:
        data = json.loads(request.body)
        contact = Contact.objects.create(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            source=data.get('source', 'organic'),
            tags=data.get('tags', [])
        )
        return JsonResponse({'success': True, 'id': contact.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def api_create_order(request):
    try:
        data = json.loads(request.body)
        contact, created = Contact.objects.get_or_create(
            email=data.get('email'),
            defaults={
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'phone': data.get('phone', ''),
                'is_buyer': True
            }
        )
        product = Product.objects.get(id=data.get('product_id'))
        order = Order.objects.create(
            contact=contact,
            product=product,
            amount=product.price,
            status='completed'
        )
        return JsonResponse({'success': True, 'order_id': order.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def api_send_broadcast(request):
    try:
        data = json.loads(request.body)
        broadcast = Broadcast.objects.create(
            subject=data.get('subject', ''),
            message=data.get('message', ''),
            segment=data.get('segment', 'all')
        )
        return JsonResponse({'success': True, 'id': broadcast.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
