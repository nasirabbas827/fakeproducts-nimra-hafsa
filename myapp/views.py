from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import user_registerForm, LoginForm, CommentForm, UserUpdateForm
from .models import user_register, Product, Comment


def register(request):
    if request.method == 'POST':
        form = user_registerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = user_registerForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = user_register.objects.get(username=username)
                if user.password == password:
                    request.session['username'] = username
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid password.')
            except user_register.DoesNotExist:
                messages.error(request, 'Username does not exist.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Comment, IPTracking
from django.contrib import messages
from .forms import CommentForm
from nltk.corpus import sentiwordnet as swn
from django.utils import timezone

from django.shortcuts import render
from .models import Product

def home(request):
    # Fetch all products
    products = Product.objects.all()

    # Calculate the sentiment score for each product
    for product in products:
        total_score = 0
        comment_count = 0
        # Loop through the product's comments and calculate the sentiment score
        for comment in product.comments.all():
            total_score += comment.sentiment_score
            comment_count += 1
        
        # Calculate average sentiment score if there are any comments
        if comment_count > 0:
            product.average_sentiment = total_score / comment_count
        else:
            product.average_sentiment = None  # No reviews

    return render(request, 'home.html', {
        'products': products,
    })


import socket
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Comment, IPTracking
from django.utils import timezone
from django.db import IntegrityError
from nltk.corpus import sentiwordnet as swn

# Function to get sentiment score and label
def get_sentiment_score(text):
    sentiment_score = 0
    sentiment_label = "Neutral"
    words = text.split()

    for word in words:
        # Get sentiment score using SentiWordNet
        synsets = swn.senti_synsets(word)
        for synset in synsets:
            sentiment_score += synset.pos_score() - synset.neg_score()

    if sentiment_score > 0:
        sentiment_label = "Positive"
    elif sentiment_score < 0:
        sentiment_label = "Negative"

    return sentiment_score, sentiment_label

def track_ip_activity(ip_address, product, comment=None):
    # Fetch or create an IPTracking record
    ip_record, created = IPTracking.objects.get_or_create(
        ip_address=ip_address,
        product=product
    )

    ip_record.review_count += 1
    ip_record.last_review_date = timezone.now()

    # Flag as fake if more than 3 reviews are detected from the same IP
    if ip_record.review_count > 3 and (comment and comment.sentiment_score > 3.0):
        ip_record.flagged_as_fake = True

    ip_record.save()  # Save the updated IPTracking object

    # Optionally, link the IPTracking record to the comment (if comment is provided)
    if comment:
        # Add the IPTracking instance to the 'comment' field on IPTracking model
        ip_record.comment = comment
        ip_record.save()


# Main view function to handle product details and comment submission
def product_details(request, product_id):
    # Fetch product using productid (not id)
    product = get_object_or_404(Product, productid=product_id)

    # Check if the user is logged in via session
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login page if not logged in

    # Handle comment submission
    if request.method == 'POST':
        text = request.POST.get('text')
        # Simulating IP address detection
        ip_address = socket.gethostbyname(socket.gethostname())

        # Get sentiment score and label
        sentiment_score, sentiment_label = get_sentiment_score(text)

        try:
            # Create and save the new comment with IP address, sentiment score, and label
            comment = Comment(
                product=product,
                username=username,
                text=text,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                ip_address=ip_address
            )
            comment.save()

            # Track IP activity for potential fake review
            track_ip_activity(ip_address, product, comment=comment)

        except IntegrityError:
            # Handle the case where the user has already commented on this product
            error_message = "You have already commented on this product."
            return render(request, 'product_details.html', {
                'error_message': error_message,
                'username': username,
                'product': product,
                'comments': product.comments.all()
            })

    # Fetch all comments for the product
    comments = product.comments.all()

    return render(request, 'product_details.html', {
        'username': username,
        'product': product,
        'comments': comments
    })


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

def update_profile(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(user_register, username=username)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'update_profile.html', {'form': form})
