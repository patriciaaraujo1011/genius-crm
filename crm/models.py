from django.contrib.auth.models import User
from django.db import models


class Pipeline(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PipelineStage(models.Model):
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, related_name="stages"
    )
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    include_in_chart = models.BooleanField(default=True)
    include_in_distribution = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class Contact(models.Model):
    SOURCE_CHOICES = [
        ("lead_magnet_freebie_a", "Lead Magnet - Freebie A"),
        ("lead_magnet_freebie_b", "Lead Magnet - Freebie B"),
        ("webinar", "Webinar"),
        ("referral", "Referral"),
        ("organic", "Organic"),
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("meta_ad", "Meta Ad"),
        ("google_ad", "Google Ad"),
        ("tiktok", "TikTok"),
        ("email", "Email"),
        ("manual", "Manual Entry"),
    ]
    PIPELINE_STAGE_CHOICES = [
        ("new_lead", "New Lead"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("proposal", "Proposal"),
        ("negotiation", "Negotiation"),
        ("closed_won", "Closed Won"),
        ("closed_lost", "Closed Lost"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    source = models.CharField(
        max_length=50, choices=SOURCE_CHOICES, default="organic"
    )
    utm_source = models.CharField(max_length=200, blank=True)
    utm_medium = models.CharField(max_length=200, blank=True)
    utm_campaign = models.CharField(max_length=200, blank=True)
    utm_content = models.CharField(max_length=200, blank=True)
    utm_term = models.CharField(max_length=200, blank=True)
    tags = models.JSONField(default=list, blank=True)
    products_purchased = models.JSONField(default=list, blank=True)
    pipeline_stage = models.CharField(
        max_length=50, choices=PIPELINE_STAGE_CHOICES, default="new_lead"
    )
    is_buyer = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            self.save()

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
            self.save()

    def add_product(self, product_name):
        if product_name not in self.products_purchased:
            self.products_purchased.append(product_name)
            self.save()


class Opportunity(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.SET_NULL, null=True, blank=True
    )
    stage = models.ForeignKey(
        PipelineStage, on_delete=models.SET_NULL, null=True, blank=True
    )
    deal_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    close_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Opp: {self.contact} - {self.stage}"


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ("course", "Course"),
        ("membership", "Membership"),
        ("digital", "Digital Product"),
        ("service", "Service"),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(
        max_length=50, choices=PRODUCT_TYPE_CHOICES, default="course"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    stripe_payment_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact} - {self.product}"


class Funnel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tag = models.CharField(
        max_length=100,
        blank=True,
        help_text="Auto-tag applied to leads from this funnel",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        self.tag = slugify(self.name).replace("-", "_")
        super().save(*args, **kwargs)


class FunnelPage(models.Model):
    PAGE_TYPE_CHOICES = [
        ("landing", "Landing/Sales Page"),
        ("order", "Order Page"),
        ("checkout", "Checkout"),
        ("upsell", "Upsell"),
        ("downsell", "Downsell"),
        ("thank_you", "Thank You"),
        ("optin", "Opt-in/Lead Magnet"),
    ]
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE)
    page_type = models.CharField(max_length=50, choices=PAGE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    headline = models.CharField(max_length=300, blank=True)
    subheadline = models.TextField(blank=True)
    cta_text = models.CharField(
        max_length=100, blank=True, default="Get Started"
    )
    countdown_hours = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.funnel.name} - {self.get_page_type_display()}"


class Module(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="modules"
    )
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ("video", "Video"),
        ("text", "Text"),
        ("audio", "Audio"),
        ("quiz", "Quiz"),
    ]
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    content_type = models.CharField(
        max_length=50, choices=CONTENT_TYPE_CHOICES, default="video"
    )
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class MemberProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "lesson"]


class GamificationPoints(models.Model):
    ACTION_CHOICES = [
        ("lesson_complete", "Complete Lesson"),
        ("module_complete", "Complete Module"),
        ("course_complete", "Complete Course"),
        ("purchase", "Purchase"),
        ("community_post", "Community Post"),
        ("streak", "Daily Streak"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    points_required = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "badge"]


class Broadcast(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    segment = models.CharField(max_length=50, default="all")
    pillar_tag = models.CharField(max_length=100, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    open_rate = models.IntegerField(default=0)

    def __str__(self):
        return self.subject


class EmailSequence(models.Model):
    name = models.CharField(max_length=200)
    trigger = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EmailSequenceStep(models.Model):
    sequence = models.ForeignKey(
        EmailSequence, on_delete=models.CASCADE, related_name="steps"
    )
    order = models.IntegerField()
    subject = models.CharField(max_length=200)
    content = models.TextField()
    delay_hours = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sequence.name} - Step {self.order}"
