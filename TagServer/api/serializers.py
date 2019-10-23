from accounts.models import CustomUser
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Process, Profile, Content, Tag, UserOutput, OutputTag
from rest_framework import serializers

from drf_writable_nested import WritableNestedModelSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class ProcessSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(read_only=True)
    number_of_profiles = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_number_of_profiles(obj):
        return obj.profile_set.count()

    @staticmethod
    def get_tags(obj):
        return TagSerializer(Tag.objects.filter(process_id=obj.pk).all(), many=True).data

    class Meta:
        model = Process
        fields = [
            'id',
            'title',
            'number_of_profiles',
            'tag_method',
            'tags',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'title',
            'is_checked',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_content(obj):
        # obj is model instance
        return ContentSerializer(Content.objects.filter(profile__id=obj.pk).all(), many=True).data

    class Meta:
        model = Profile
        fields = [
            'id',
            'is_multi_content',
            'content',
        ]


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = [
            'url',
            'title',
            'type',
        ]


class OutputTagSerializer(WritableNestedModelSerializer):
    class Meta:
        model = OutputTag
        fields=('title', )


class UserOutputSerializer(OutputTagSerializer):
    tags = OutputTagSerializer(many=True)

    class Meta:
        model = UserOutput
        read_only_fields = ('user', 'id', )
        fields = [
            'id',
            'process_id',
            'profile_id',
            'user',
            'tags',
        ]

