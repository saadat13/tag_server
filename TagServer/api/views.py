from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from .models import Process, Profile, Content, Tag, UserOutput
from .serializers import ProcessSerializer, ProfilePackage, ProfileSerializer, \
    ContentSerializer, TagSerializer, ProfilePackageSerializer, UserOutputSerializer, MyTokenObtainPairSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics


class ProcessAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = ProcessSerializer
    queryset = Process.objects.all()


class UserOutputAPIView(ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = UserOutputSerializer
    queryset = UserOutput.objects.all()


class PackageProfileAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePackageSerializer
    queryset = ProfilePackage.objects.all()

    def get_queryset(self):
        return ProfilePackage.objects.all()

    def get(self, *args, **kwargs):
        data = self.get_serializer(self.get_queryset(), many=True).data
        flag = (len(data) != 0)
        if flag:
            print(data)
            has_next = data[0]['has_next']
            process_id = data[0]['process']
        else:
            return JsonResponse({"info": "there is no profile package!"})
        serialized_profiles = ProfileSerializer(ProfilePackage.objects.filter(process__id=self.kwargs['pid']).first().profile_set.all(), many=True).data
        return JsonResponse(
            {
                'has_next': has_next,
                'process': process_id,
                'profiles': serialized_profiles
            }
        )

