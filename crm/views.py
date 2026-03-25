from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from .models import (
    Contact, Product, Order, Funnel, FunnelPage,
    Module, Lesson, MemberProgress, GamificationPoints,
    Badge, UserBadge, Broadcast, EmailSequence, EmailSequenceStep,
    Pipeline, PipelineStage, Opportunity
)
from .validators import validate_email, get_country_from_phone
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


def optin_page(request, slug=None):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        source = request.POST.get('source', 'organic')
        tag = request.POST.get('tag', '')
        
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return render(request, 'optin.html', {
                'error': error_msg,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'slug': slug
            })
        
        country = get_country_from_phone(phone)
        
        tags = [tag] if tag else []
        
        contact, created = Contact.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'country': country,
                'source': source,
                'tags': tags,
                'pipeline_stage': 'new_lead'
            }
        )
        
        if not created:
            contact.first_name = first_name
            contact.last_name = last_name
            contact.phone = phone
            contact.country = country
            for t in tags:
                if t not in contact.tags:
                    contact.tags.append(t)
            contact.save()
        
        return redirect('optin_thankyou')
    
    return render(request, 'optin.html', {'slug': slug})


def optin_thankyou(request):
    return render(request, 'optin_thankyou.html')


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
        email = data.get('email', '').strip()
        
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg})
        
        phone = data.get('phone', '')
        country = get_country_from_phone(phone)
        tags = data.get('tags', [])
        source = data.get('source', 'organic')
        
        contact, created = Contact.objects.get_or_create(
            email=email,
            defaults={
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'phone': phone,
                'country': country,
                'source': source,
                'tags': tags,
                'pipeline_stage': 'new_lead'
            }
        )
        
        if not created:
            return JsonResponse({'success': False, 'error': 'Contact with this email already exists'})
        
        return JsonResponse({'success': True, 'id': contact.id, 'created': True})
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


@login_required
def pipeline_list(request):
    pipelines = Pipeline.objects.prefetch_related('stages').all()
    return render(request, 'pipeline_list.html', {'pipelines': pipelines})


@login_required
def pipeline_board(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id)
    stages = pipeline.stages.all()
    opportunities = Opportunity.objects.filter(pipeline=pipeline).select_related('contact', 'stage')
    contacts = Contact.objects.all()
    return render(request, 'pipeline_board.html', {
        'pipeline': pipeline,
        'stages': stages,
        'opportunities': opportunities,
        'contacts': contacts
    })


@require_http_methods(["POST"])
def api_create_pipeline(request):
    try:
        data = json.loads(request.body)
        pipeline = Pipeline.objects.create(name=data.get('name', 'New Pipeline'))
        
        default_stages = ['New Lead', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        for i, stage_name in enumerate(default_stages):
            PipelineStage.objects.create(pipeline=pipeline, name=stage_name, order=i)
        
        return JsonResponse({'success': True, 'id': pipeline.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def api_create_opportunity(request):
    try:
        data = json.loads(request.body)
        contact = Contact.objects.get(id=data.get('contact_id'))
        pipeline = Pipeline.objects.get(id=data.get('pipeline_id'))
        stage = pipeline.stages.first()
        
        opportunity = Opportunity.objects.create(
            contact=contact,
            pipeline=pipeline,
            stage=stage,
            deal_value=data.get('deal_value', 0)
        )
        return JsonResponse({'success': True, 'id': opportunity.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def api_update_opportunity_stage(request):
    try:
        data = json.loads(request.body)
        opportunity = Opportunity.objects.get(id=data.get('opportunity_id'))
        stage = PipelineStage.objects.get(id=data.get('stage_id'))
        opportunity.stage = stage
        opportunity.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
