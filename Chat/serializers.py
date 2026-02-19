from dataclasses import field
from .models import Room, Message, Profile
from rest_framework import serializers
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'pfp']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }   

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'content', 'created_at']
    
class RoomSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'users', 'created_at', 'name']

    def get_name(self, obj):
        # Assuming request context is passed to serializer
        if 'request' in self.context:
            request_user = self.context['request'].user
            # Filter users to find the one that is NOT the request user
            other_user = obj.users.exclude(id=request_user.id).first()
            if other_user:
                return other_user.username
        # Fallback if no other user or context missing
        return f"Room #{obj.id}"