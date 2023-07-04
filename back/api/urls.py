
from django.contrib import admin
from django.urls import path, include
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index),
    path('products', views.product_view.as_view()),
    path('products/<pk>', views.product_view.as_view()),
    # path('checkout',views.checkout),
    # path('login/', TokenObtainPairView.as_view()),
    # path('checkout', views.CartView.as_view()),
    # path('image/', views.DynamicImageView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


