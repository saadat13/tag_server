from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from .models import Process, Profile, Content, Tag, UserOutput
from .serializers import ProcessSerializer, ProfilePackage,\
    ProfileSerializer, ProfilePackageSerializer, UserOutputSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import  generics
from datetime import datetime, timedelta



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

    def get_queryset(self):
        return UserOutput.objects.all()


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



