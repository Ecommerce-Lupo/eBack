"""
Product views
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from core.models import Product, User

from .serializers import ProductSerializer, ProductByIdSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    """Only admin users actions"""

    @action(methods=['post'], detail=False)
    def add_product(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    """All users actions"""

    @action(methods=['get'], detail=False)
    def get_products(self, request):

        return Response({'data': self.serializer_class(self.queryset, many=True).data}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_product_by_id(self, request):
        product_id = request.query_params.get('id')
        product = Product.objects.get(id=product_id)

        serialized_product = ProductByIdSerializer(product)

        return Response(serialized_product.data, status=status.HTTP_200_OK)
    
        
    # TODO: Falta implementar que solo haga put si es un admin
    def put(self, request, *args, **kwargs):
        """Handle updating an object"""
        product_id = request.data.get('id')
        product = self.queryset.get(id=product_id)
        # A continuación, se debe recuperar el tamaño porque django no deja no actualizarlo a pesar de no ser nulo
        product_size = product.size
        request_data = request.data.copy() # request.data es inmutable
        request_data.update({'size': product_size}) # se updatea size con el valor original
        
        # Flujo normal
        data_serializer = ProductSerializer(product, data=request_data)
        if data_serializer.is_valid():
            data_serializer.save()
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'method': 'PUT', "id": product.id, 'data': data_serializer.data}, status=status.HTTP_200_OK)
    
    @action(methods=['put'], detail=False)
    def stock_update(self, request, *args, **kwargs):
        """Handle updating ONLY stock of a product"""
        product_id = request.data.get('id')
        product = self.queryset.get(id=product_id)
        new_stock = request.data.get('quantity')
        data_serializer = ProductSerializer(product, data={'quantity': new_stock}, partial=True)
        if data_serializer.is_valid():
            data_serializer.save()
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': data_serializer.data}, status=status.HTTP_200_OK)