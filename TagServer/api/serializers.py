from .models import Process, ProfilePackage, Profile, Content, Tag, UserOutput, OutputTag
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user.is_staff)
        # Add custom claims
        # token['name'] = user.name
        # ...

        return token


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        # list_serializer_class = CollegeListSerializer
        fields = [
            'id',
            'title',
            'number_of_profiles',
            'details',
            'tagging_method',
        ]


class TagSerializer(serializers.ModelSerializer):
    process = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_process(obj):
        # obj is model instance
        return obj.profile.packageProfile.process.id

    class Meta:
        model = Tag
        fields = [
            'id',
            'process',
            'profile',
            'title',
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


class OutputTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputTag
        fields=[
            'id',
            'tag_title',
        ]

class UserOutputSerializer(serializers.ModelSerializer):
    # tags = serializers.SerializerMethodField()
    #
    # @staticmethod
    # def get_tags(obj):
    #     # obj is model instance
    #     obj.output_tag_set.all()

    class Meta:
        model = UserOutput
        fields = [
            'id',
            'process_id',
            'profile_package_id',
            'profile_id',
            # 'tags',
        ]

    # def validate(self, data):
    #     tag = data.get('tag_title', None)
    #     if tag == "":
    #         tag = None
    #     if tag is None:
    #         raise serializers.ValidationError("tag is empty!")
    #     elif len(tag) > 20:
    #         raise serializers.ValidationError("maximum length exceeded!")
    #     return data
