
from rest_framework import serializers
from core.models import Product

class ProductSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.name

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'user_name', 'user', 'created_at', 'updated_at', 'image']


class ProductByIdSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.name

    class Meta:
        model = Product
        fields = [ 'id', 'name', 'description', 'price', 'created_at', 'updated_at', 'image', 'user_name']
        read_only_fields = ['user_name', 'user', 'created_at', 'updated_at']