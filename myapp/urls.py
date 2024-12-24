from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('post_comment/<int:product_id>/', views.product_details, name='post_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
