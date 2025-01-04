
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the user's password before saving
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', User.USER),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


