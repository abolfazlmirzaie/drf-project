from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter



app_name = 'api'
urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view(), name='products'),
    path('products/info', views.ProductInfoAPIView.as_view(), name='product_info'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='products_detail'),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls

