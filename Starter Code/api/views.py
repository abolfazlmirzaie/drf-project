from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilter, ProductFilter, OrderFilter
from api.models import Order, OrderItem, Product
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
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
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs




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





