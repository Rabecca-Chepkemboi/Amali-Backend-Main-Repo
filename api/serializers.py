from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from register.models import CustomUser, Athlete, Sponsor
from donation.models import Donation
from comments.models import Comment
from contact.models import ContactMessage
# from video.models import Video

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'full_name',
            'role',
            'groups',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)
        if confirm_password and validated_data['password'] != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = '__all__'

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:

        model = Sponsor
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('full_name', 'comment', 'likes')



class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ('name','email','message')

# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = '__all__'
        