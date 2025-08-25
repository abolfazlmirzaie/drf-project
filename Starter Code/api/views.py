from django.db.models import Max
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
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


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = Product.objects.get(pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)




class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer



# @api_view(['GET'])
# def order_list(request):
#     order = Order.objects.prefetch_related('items__product',)
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)





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





