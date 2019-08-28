from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from .models import Process, UserOutput
from .serializers import ProcessSerializer, ProfilePackage, ProfilePackageSerializer, UserOutputSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import time
from django.http import Http404


class ProcessAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = ProcessSerializer
    queryset = Process.objects.all()

    def get_queryset(self):
        user = self.request.user
        role = user.role
        return Process.objects.exclude(users=user).all()


class UserOutputAPIView(ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = UserOutputSerializer
    queryset = UserOutput.objects.all().order_by("-id")

    def post(self, request, *args, **kwargs):
        data = request.data
        process_id = data['process_id']
        package_profile_id = data['package_profile_id']
        profile_id = data['profile_id']
        try:
            current_process = Process.objects.get(id=process_id)
            current_package = ProfilePackage.objects.get(id=package_profile_id)

            current_process.users.add(request.user)  #adding current user to users list tagged this profile
            role = request.user.role
            if role is "expert":
                current_package.is_tagged = True
                current_package.save()
            elif role is "full_expert":
                current_package.is_valid = True
                current_package.save()
        except Exception as e:
            print(str(e))
        return super(UserOutputAPIView, self).post(request, *args, **kwargs)


class PackageProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePackageSerializer
    queryset = ProfilePackage.objects.all()

    def get_object(self):
        package = ProfilePackage.objects.filter(process__id=self.kwargs['pid'], status="available", is_tagged=False).order_by('id').first()
        print(package)
        if package is not None:
            package.status = "blocked"
            millis = int(round(time.time() * 1000))
            package.expire_date = str(millis + 1*60*60*1000)  # set expire date to 1 hour after getting package
            package.save()
            return package
        else:
            raise Http404

#
# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def block_profile(request, *args, **kwargs):
#     pid = kwargs['pid']
#     id = kwargs['id']
#     i = kwargs['i']
#     try:
#         profile = Profile.objects.filter(id=i, packageProfile__id=id, packageProfile__process__id=pid).first()
#         status = profile.status
#         if status == "blocked":
#             return JsonResponse({"error": "profile is already blocked!"})
#         elif status == "tagged":
#             return JsonResponse({"error": "profile is already tagged, refresh your profile list"})
#         else:
#             profile.status = "blocked"
#             profile.expire_date = datetime.now() + timedelta(hours=1)
#             profile.save()
#             return JsonResponse({"error": "blocked successfully"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})
#
#
# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def unblock_profile(request, *args, **kwargs):
#     pid = kwargs['pid']
#     id = kwargs['id']
#     i = kwargs['i']
#     try:
#         profile = Profile.objects.filter(id=i, packageProfile__id=id, packageProfile__process__id=pid).first()
#         status = profile.status
#         if status == "blocked":
#             profile.status = "unblocked"
#             profile.expire_date = None
#             profile.save()
#             return JsonResponse({"error": "unblocked successfully"})
#         elif status == "tagged":
#             return JsonResponse({"error": "process is already tagged, refresh your process list"})
#         else:
#             return JsonResponse({"error": "process is already available, refresh your process list"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})
