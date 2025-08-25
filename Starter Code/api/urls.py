from django.urls import path
from . import views
app_name = 'api'
urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view(), name='products'),
    path('products/info', views.ProductInfoAPIView.as_view(), name='product_info'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='products_detail'),
    path('orders/', views.OrderListAPIView.as_view(), name='order_list'),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='order_list'),

]

