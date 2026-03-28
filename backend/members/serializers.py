from django.contrib.auth.models import User
from rest_framework import serializers

from .models import MemberProfile


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = MemberProfile
        fields = [
            "id",
            "user",
            "main_li",
            "birthday",
            "bio",
            "status",
            "role",
            "can_edit_profile",
            "created_at",
        ]