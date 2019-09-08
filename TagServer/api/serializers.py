from accounts.models import CustomUser
from .models import Process, ProfilePackage, Profile, Content, Tag, UserOutput, OutputTag
from rest_framework import serializers

from drf_writable_nested import WritableNestedModelSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = [
            'id',
            'title',
            'number_of_profiles',
            'details',
            'tagging_method',
        ]


class TagSerializer(serializers.ModelSerializer):
    process = serializers.SerializerMethodField(read_only=True)
    users = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_process(obj):
        # obj is model instance
        return obj.profile.packageProfile.process.id

    @staticmethod
    def get_users(obj):
        return CustomUserSerializer(obj.users.all(), many=True).data

    class Meta:
        model = Tag
        fields = [
            'id',
            'process',
            'profile',
            'title',
            'percent',
            'users',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_tag(obj):
        # obj is model instance
        return TagSerializer(Tag.objects.filter(profile__id=obj.id).all(), many=True).data

    @staticmethod
    def get_content(obj):
        # obj is model instance
        return ContentSerializer(Content.objects.filter(profile__id=obj.id).all(), many=True).data

    class Meta:
        model = Profile
        fields = [
            'id',
            'is_multi_content',
            'tag',
            'content',
        ]


class ProfilePackageSerializer(serializers.ModelSerializer):
    profiles = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_profiles(obj):
        # obj is model instance
        return ProfileSerializer(Profile.objects.filter(packageProfile__id=obj.id).all(), many=True).data

    class Meta:
        model = ProfilePackage
        fields = [
            'id',
            'process',
            'has_next',
            'is_tagged',
            'is_valid',
            'status',
            'expire_date',
            'profiles',
        ]


class ContentSerializer(serializers.ModelSerializer):
    process = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_process(obj):
        # obj is model instance
        return obj.profile.packageProfile.process.id

    class Meta:
        model = Content
        fields = [
            'id',
            'process',
            'profile',
            'url',
            'title',
            'type',
        ]


class OutputTagSerializer(WritableNestedModelSerializer):
    class Meta:
        model = OutputTag
        fields = [
            'id',
            'tag_title'
        ]


class UserOutputSerializer(OutputTagSerializer):
    tags = OutputTagSerializer(many=True)

    class Meta:
        model = UserOutput
        fields = [
            'id',
            'process_id',
            'profile_package_id',
            'profile_id',
            'tags',
        ]

