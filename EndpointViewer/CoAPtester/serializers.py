from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Post

class CoAPtesterSerializer(serializers.ModelSerializer):
    """
    Adds a serializer interface for any of the required fields in the model.
    """
    # class Meta:
        # model = User
        # fields = ['username', 'email', 'groups']
