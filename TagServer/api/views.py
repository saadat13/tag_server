from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from .models import Process, Profile, Content, Tag, UserOutput
from .serializers import ProcessSerializer, ProfilePackage,\
    ProfileSerializer, ProfilePackageSerializer, UserOutputSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import  generics
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
import time
from django.http import Http404
import json
from .serializers import OutputTagSerializer

class ProcessAPIView(ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = ProcessSerializer
    queryset = Process.objects.all()


class UserOutputAPIView(ListAPIView, generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = UserOutputSerializer
    queryset = UserOutput.objects.all()

    # def perform_create(self, request):
    #
    #     super().perform_create(self, request)

    def get_queryset(self):
        return UserOutput.objects.all()


class PackageProfileAPIView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfilePackageSerializer
    queryset = ProfilePackage.objects.all()

    def get_object(self):
        package = ProfilePackage.objects.filter(process__id=self.kwargs['pid'], status="available", is_tagged=False).order_by('id').first()
        print(package)
        if package != None:
            # package.status = "blocked"
            millis = int(round(time.time() * 1000))
            package.expire_date = str(millis + 1*60*60*1000)
            package.save()
            return package
        else:
            raise Http404


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def block_profile(request, *args, **kwargs):
    pid = kwargs['pid']
    id = kwargs['id']
    i = kwargs['i']
    try:
        profile = Profile.objects.filter(id=i, packageProfile__id=id, packageProfile__process__id=pid).first()
        status = profile.status
        if status == "blocked":
            return JsonResponse({"error": "profile is already blocked!"})
        elif status == "tagged":
            return JsonResponse({"error": "profile is already tagged, refresh your profile list"})
        else:
            profile.status = "blocked"
            profile.expire_date = datetime.now() + timedelta(hours=1)
            profile.save()
            return JsonResponse({"error": "blocked successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def unblock_profile(request, *args, **kwargs):
    pid = kwargs['pid']
    id = kwargs['id']
    i = kwargs['i']
    try:
        profile = Profile.objects.filter(id=i, packageProfile__id=id, packageProfile__process__id=pid).first()
        status = profile.status
        if status == "blocked":
            profile.status = "unblocked"
            profile.expire_date = None
            profile.save()
            return JsonResponse({"error": "unblocked successfully"})
        elif status == "tagged":
            return JsonResponse({"error": "process is already tagged, refresh your process list"})
        else:
            return JsonResponse({"error": "process is already available, refresh your process list"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
