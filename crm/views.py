import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import (
    Broadcast,
    Contact,
    EmailSequence,
    Funnel,
    Opportunity,
    Order,
    OrderBump,
    Pipeline,
    PipelineStage,
    Product,
)
from .stripe_utils import create_order_bump_session
from .validators import get_country_from_phone, validate_email


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid credentials")
    return render(request, "login.html")


def optin_page(request, slug=None):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        phone_code = request.POST.get("phone_code", "")
        source = request.POST.get("source", "organic")
        request.POST.get("tag", "")

        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return render(
                request,
                "optin.html",
                {
                    "error": error_msg,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": f"{phone_code} {phone}" if phone_code else phone,
                    "slug": slug,
                },
            )

        country = get_country_from_phone(f"{phone_code}{phone}")
        full_phone = f"{phone_code} {phone}" if phone_code else phone

        utm_source = request.GET.get("utm_source", "")
        utm_medium = request.GET.get("utm_medium", "")
        utm_campaign = request.GET.get("utm_campaign", "")
        utm_content = request.GET.get("utm_content", "")
        utm_term = request.GET.get("utm_term", "")

        if not source or source == "organic":
            if utm_source:
                source = utm_source
            elif utm_medium:
                source = utm_medium

        from datetime import datetime

        tags_to_add = [
            "opt-in-1",  # 1. Template tag
            slug or "main",  # 2. Funnel/slug tag
            source,  # 3. Source tag (from UTM or default)
            datetime.now()
            .strftime("%B-%Y")
            .lower(),  # 4. Date tag (e.g., march-2026)
            "lead-magnet",  # 5. Lead magnet tag
        ]

        if utm_campaign:
            tags_to_add.append(f"campaign-{utm_campaign}")
        if utm_source:
            tags_to_add.append(f"source-{utm_source}")

        contact, created = Contact.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "phone": full_phone,
                "country": country,
                "source": source,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign,
                "utm_content": utm_content,
                "utm_term": utm_term,
                "tags": tags_to_add,
                "pipeline_stage": "new_lead",
            },
        )

        if not created:
            contact.first_name = first_name
            contact.last_name = last_name
            contact.phone = full_phone
            contact.country = country
            if utm_source:
                contact.utm_source = utm_source
            if utm_medium:
                contact.utm_medium = utm_medium
            if utm_campaign:
                contact.utm_campaign = utm_campaign
            for t in tags_to_add:
                if t not in contact.tags:
                    contact.tags.append(t)
            contact.save()

        return redirect("/opt-in/thank-you/?submitted=1")

    return render(request, "optin.html", {"slug": slug})


def optin_thankyou(request):
    return render(request, "optin_thankyou.html")


@login_required
def dashboard(request):
    total_contacts = Contact.objects.count()
    buyer_contacts = Contact.objects.filter(is_buyer=True).count()
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status="completed").count()
    total_revenue = (
        Order.objects.filter(status="completed").aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    total_products = Product.objects.count()
    active_funnels = Funnel.objects.filter(is_active=True).count()
    total_broadcasts = Broadcast.objects.count()

    recent_contacts = Contact.objects.order_by("-created_at")[:5]
    recent_orders = Order.objects.select_related(
        "contact", "product"
    ).order_by("-created_at")[:5]
    top_products = Product.objects.annotate(
        order_count=Count("order")
    ).order_by("-order_count")[:5]

    context = {
        "total_contacts": total_contacts,
        "buyer_contacts": buyer_contacts,
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "total_revenue": total_revenue,
        "total_products": total_products,
        "active_funnels": active_funnels,
        "total_broadcasts": total_broadcasts,
        "recent_contacts": recent_contacts,
        "recent_orders": recent_orders,
        "top_products": top_products,
    }
    return render(request, "dashboard.html", context)


@login_required
def contacts(request):
    contacts = Contact.objects.order_by("-created_at")
    return render(request, "contacts.html", {"contacts": contacts})


@login_required
def products(request):
    products = Product.objects.order_by("-created_at")
    return render(request, "products.html", {"products": products})


@login_required
def orders(request):
    orders = Order.objects.select_related("contact", "product").order_by(
        "-created_at"
    )
    return render(request, "orders.html", {"orders": orders})


@login_required
def funnels(request):
    funnels = Funnel.objects.prefetch_related("funnelpage_set").order_by(
        "-created_at"
    )
    return render(request, "funnels.html", {"funnels": funnels})


@login_required
def funnel_templates(request):
    return render(request, "funnel_templates.html")


@login_required
def funnel_detail(request, slug):
    funnel = Funnel.objects.prefetch_related("funnelpage_set").get(slug=slug)
    pages = funnel.funnelpage_set.all()
    return render(
        request, "funnel_detail.html", {"funnel": funnel, "pages": pages}
    )


@login_required
def courses(request):
    products = Product.objects.filter(product_type="course")
    return render(request, "courses.html", {"products": products})


@login_required
def course_detail(request, slug):
    product = Product.objects.prefetch_related("modules__lessons").get(
        slug=slug
    )
    return render(request, "course_detail.html", {"product": product})


@login_required
def broadcast(request):
    broadcasts = Broadcast.objects.order_by("-sent_at")[:20]
    return render(request, "broadcast.html", {"broadcasts": broadcasts})


@login_required
def sequences(request):
    sequences = EmailSequence.objects.prefetch_related("steps").all()
    return render(request, "sequences.html", {"sequences": sequences})


@require_http_methods(["POST"])
def api_add_contact(request):
    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()

        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return JsonResponse({"success": False, "error": error_msg})

        phone = data.get("phone", "")
        country = get_country_from_phone(phone)
        tags = data.get("tags", [])
        source = data.get("source", "organic")

        contact, created = Contact.objects.get_or_create(
            email=email,
            defaults={
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "phone": phone,
                "country": country,
                "source": source,
                "tags": tags,
                "pipeline_stage": "new_lead",
            },
        )

        if not created:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Contact with this email already exists",
                }
            )

        return JsonResponse(
            {"success": True, "id": contact.id, "created": True}
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@require_http_methods(["POST"])
def api_create_order(request):
    try:
        data = json.loads(request.body)
        contact, created = Contact.objects.get_or_create(
            email=data.get("email"),
            defaults={
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "phone": data.get("phone", ""),
                "is_buyer": True,
            },
        )
        product = Product.objects.get(id=data.get("product_id"))
        order = Order.objects.create(
            contact=contact,
            product=product,
            amount=product.price,
            status="completed",
        )
        return JsonResponse({"success": True, "order_id": order.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@require_http_methods(["POST"])
def api_send_broadcast(request):
    try:
        data = json.loads(request.body)
        broadcast = Broadcast.objects.create(
            subject=data.get("subject", ""),
            message=data.get("message", ""),
            segment=data.get("segment", "all"),
        )
        return JsonResponse({"success": True, "id": broadcast.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def pipeline_list(request):
    pipelines = Pipeline.objects.prefetch_related("stages").all()
    return render(request, "pipeline_list.html", {"pipelines": pipelines})


@login_required
def pipeline_board(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id)
    stages = pipeline.stages.all()
    opportunities = Opportunity.objects.filter(
        pipeline=pipeline
    ).select_related("contact", "stage")
    contacts = Contact.objects.all()
    return render(
        request,
        "pipeline_board.html",
        {
            "pipeline": pipeline,
            "stages": stages,
            "opportunities": opportunities,
            "contacts": contacts,
        },
    )


@require_http_methods(["POST"])
def api_create_pipeline(request):
    try:
        data = json.loads(request.body)
        pipeline = Pipeline.objects.create(
            name=data.get("name", "New Pipeline")
        )

        default_stages = [
            "New Lead",
            "Contacted",
            "Qualified",
            "Proposal",
            "Negotiation",
            "Closed Won",
            "Closed Lost",
        ]
        for i, stage_name in enumerate(default_stages):
            PipelineStage.objects.create(
                pipeline=pipeline, name=stage_name, order=i
            )

        return JsonResponse({"success": True, "id": pipeline.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@require_http_methods(["POST"])
def api_create_opportunity(request):
    try:
        data = json.loads(request.body)
        contact = Contact.objects.get(id=data.get("contact_id"))
        pipeline = Pipeline.objects.get(id=data.get("pipeline_id"))
        stage = pipeline.stages.first()

        opportunity = Opportunity.objects.create(
            contact=contact,
            pipeline=pipeline,
            stage=stage,
            deal_value=data.get("deal_value", 0),
        )
        return JsonResponse({"success": True, "id": opportunity.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@require_http_methods(["POST"])
def api_update_opportunity_stage(request):
    try:
        data = json.loads(request.body)
        opportunity = Opportunity.objects.get(id=data.get("opportunity_id"))
        stage = PipelineStage.objects.get(id=data.get("stage_id"))
        opportunity.stage = stage
        opportunity.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def funnel_landing(request, slug):
    funnel = get_object_or_404(Funnel, slug=slug, is_active=True)
    landing_page = funnel.funnelpage_set.filter(page_type="landing").first()
    main_product = Product.objects.filter(is_active=True).first()

    context = {
        "funnel": funnel,
        "page": landing_page,
        "product": main_product,
        "order_url": f"/funnel/{slug}/order/",
    }
    return render(request, "funnel/templates/sales_template_1.html", context)


def funnel_order(request, slug):
    funnel = get_object_or_404(Funnel, slug=slug, is_active=True)
    order_page = funnel.funnelpage_set.filter(page_type="order").first()
    main_product = funnel.funnelpage_set.filter(page_type="order").first()
    order_bumps = (
        funnel.order_bumps.filter(is_active=True)
        .order_by("order")
        .select_related("product")
    )

    context = {
        "funnel": funnel,
        "page": order_page,
        "main_product": main_product,
        "order_bumps": order_bumps,
    }
    return render(request, "funnel/order.html", context)


@require_http_methods(["POST"])
def funnel_checkout(request, slug):
    funnel = get_object_or_404(Funnel, slug=slug, is_active=True)
    product_id = request.POST.get("product_id")
    bump_ids = request.POST.getlist("bump_ids")
    email = request.POST.get("email", "")

    product = get_object_or_404(Product, id=product_id)
    bump_products = OrderBump.objects.filter(
        id__in=bump_ids, funnel=funnel, is_active=True
    ).select_related("product")

    base_url = request.build_absolute_uri("/")[:-1]
    success_url = f"{base_url}/funnel/{slug}/thank-you/"
    cancel_url = f"{base_url}/funnel/{slug}/order/"

    metadata = {
        "funnel_slug": slug,
        "product_id": str(product.id),
        "bump_ids": ",".join([str(b.id) for b in bump_products]),
        "contact_email": email,
    }

    try:
        session = create_order_bump_session(
            main_product=product,
            bump_products=list(bump_products),
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=email,
            metadata=metadata,
        )
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, f"Checkout error: {e!s}")
        return redirect("funnel_order", slug=slug)


def funnel_thankyou(request, slug):
    funnel = get_object_or_404(Funnel, slug=slug)
    session_id = request.GET.get("session_id")

    context = {
        "funnel": funnel,
        "session_id": session_id,
    }
    return render(request, "funnel/thank-you.html", context)


def funnel_upsell(request, slug):
    funnel = get_object_or_404(Funnel, slug=slug, is_active=True)
    upsell_page = funnel.funnelpage_set.filter(page_type="upsell").first()

    context = {
        "funnel": funnel,
        "page": upsell_page,
    }
    return render(request, "funnel/upsell.html", context)


def offer_expired(request):
    return render(request, "funnel/offer-expired.html")


@require_http_methods(["POST"])
def stripe_webhook(request):
    import stripe

    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_successful_payment(session)

    return JsonResponse({"status": "success"})


def handle_successful_payment(session):
    metadata = session.get("metadata", {})
    funnel_slug = metadata.get("funnel_slug")
    product_id = metadata.get("product_id")
    contact_email = metadata.get("contact_email")

    if not product_id:
        return

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return

    contact, _ = Contact.objects.get_or_create(
        email=contact_email,
        defaults={
            "source": "checkout",
        },
    )
    contact.is_buyer = True
    if funnel_slug:
        contact.add_tag(funnel_slug)
    contact.add_product(product.name)
    contact.save()

    Order.objects.create(
        contact=contact,
        product=product,
        amount=product.price,
        status="completed",
        stripe_payment_id=session.get("id", ""),
    )
