from django.db.models import Max
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from api.filters import ProductFilter, InStockFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import viewsets





class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'pagenumber'
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 7


    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilter,
    )

    
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'price')

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#
#
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [
#         IsAuthenticated,
#     ]
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)





class ProductInfoAPIView(APIView):
    def get(self, request):
        product = Product.objects.all()
        serializer = ProductInfoSerializer({
            'product': product,
            'count': len(product),
            'max_price': product.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(serializer.data)


# @api_view(['GET'])
# def product_info(request):
#     product = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'product': product,
#         'count': len(product),
#         'max_price': product.aggregate(max_price=Max('price'))['max_price'],
#     })
#     return Response(serializer.data)





