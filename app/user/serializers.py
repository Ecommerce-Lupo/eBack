"""
Serializers for the user app.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  """Serializer for the users object"""


  class Meta:
    model = get_user_model()
    fields = ['email', 'password', 'name', 'is_superuser']
    extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

  def create(self, validated_data):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**validated_data)
  
  def validate_name(self, value):
    if len(value) < 5 or len(value) > 50:
        raise serializers.ValidationError("El nombre debe tener entre 5 y 50 caracteres")
    return value