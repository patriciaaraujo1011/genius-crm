from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    SOURCE_CHOICES = [
        ('lead_magnet', 'Lead Magnet'),
        ('webinar', 'Webinar'),
        ('referral', 'Referral'),
        ('organic', 'Organic'),
        ('instagram', 'Instagram'),
        ('paid_ad', 'Paid Ad'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='organic')
    tags = models.JSONField(default=list, blank=True)
    is_buyer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('course', 'Course'),
        ('membership', 'Membership'),
        ('digital', 'Digital Product'),
        ('service', 'Service'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES, default='course')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_payment_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.contact} - {self.product}"


class Funnel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class FunnelPage(models.Model):
    PAGE_TYPE_CHOICES = [
        ('landing', 'Landing/Sales Page'),
        ('order', 'Order Page'),
        ('checkout', 'Checkout'),
        ('upsell', 'Upsell'),
        ('downsell', 'Downsell'),
        ('thank_you', 'Thank You'),
        ('optin', 'Opt-in/Lead Magnet'),
    ]
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE)
    page_type = models.CharField(max_length=50, choices=PAGE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    headline = models.CharField(max_length=300, blank=True)
    subheadline = models.TextField(blank=True)
    cta_text = models.CharField(max_length=100, blank=True, default='Get Started')
    countdown_hours = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.funnel.name} - {self.get_page_type_display()}"


class Module(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('quiz', 'Quiz'),
    ]
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES, default='video')
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
        unique_together = ['user', 'lesson']


class GamificationPoints(models.Model):
    ACTION_CHOICES = [
        ('lesson_complete', 'Complete Lesson'),
        ('module_complete', 'Complete Module'),
        ('course_complete', 'Complete Course'),
        ('purchase', 'Purchase'),
        ('community_post', 'Community Post'),
        ('streak', 'Daily Streak'),
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
        unique_together = ['user', 'badge']


class Broadcast(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    segment = models.CharField(max_length=50, default='all')
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
    sequence = models.ForeignKey(EmailSequence, on_delete=models.CASCADE, related_name='steps')
    order = models.IntegerField()
    subject = models.CharField(max_length=200)
    content = models.TextField()
    delay_hours = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.sequence.name} - Step {self.order}"
