from django.db import models
from django.utils import timezone

class user_register(models.Model):
    id = models.AutoField(primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.username

from django.db import models
from django.utils import timezone

class Product(models.Model):   
    productid = models.AutoField(primary_key=True)   
    name = models.CharField(max_length=255)  # Renamed from title
    description = models.TextField()
    picture = models.ImageField(upload_to='product_images/', null=True, blank=True)  # New field
    price = models.DecimalField(max_digits=10, decimal_places=2)  # New field
    quantity = models.PositiveIntegerField()  # New field
    added_date = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone

class Comment(models.Model):
    commentid = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_label = models.CharField(max_length=10, null=True, blank=True)
    ip_address = models.GenericIPAddressField(default='0.0.0.0')  # New field to track IP address

    def __str__(self):
        return f'Comment by {self.username} on {self.product.name}'


# IPTracking model to track reviews from specific IPs
class IPTracking(models.Model):
    ip_id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField()
    product = models.ForeignKey('Product', related_name='ip_tracking', on_delete=models.CASCADE)
    review_count = models.IntegerField(default=0)  # Tracks the number of reviews from this IP for a product
    flagged_as_fake = models.BooleanField(default=False)  # Flag if the IP is considered suspicious
    last_review_date = models.DateTimeField(null=True, blank=True)  # Date of the last review from this IP
    comment = models.ForeignKey('Comment', related_name='ip_tracking', null=True, blank=True, on_delete=models.CASCADE)  # Link to the Comment model

    def __str__(self):
        return f"IP {self.ip_address} tracked for product {self.product.name}"

