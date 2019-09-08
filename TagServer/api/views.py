from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from accounts.models import CustomUser
from .models import Process, UserOutput, Tag
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
        if role == "full_expert":
            return Process.objects.exclude(users=user).filter(profilepackage__is_tagged=True).all()
        return Process.objects.exclude(users=user).all()


class UserOutputAPIView(ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = UserOutputSerializer
    queryset = UserOutput.objects.all().order_by("-id")

    def post(self, request, *args, **kwargs):
        data = request.data
        process_id = int(data['process_id'])
        package_profile_id = int(data['profile_package_id'])
        tags = data['tags']
        profile_id = int(data['profile_id'])
        try:
            current_process = Process.objects.get(id=process_id)
            current_package = ProfilePackage.objects.get(id=package_profile_id)
            current_process.users.add(request.user) #adding current user to users list tagged this profile
            current_process.save()
            total_experts = CustomUser.objects.filter(role="expert").count()
            print(str(total_experts))
            for tag in tags:
                t = Tag.objects \
                    .get(title=tag['tag_title'], profile_id=profile_id, profile__packageProfile__id = package_profile_id)
                if t is not None:
                    t.users.add(request.user)
                    t.save()
                    if total_experts != 0:
                        percent = int(round((t.users.all().count()*100 / total_experts)))
                        t.percent = percent
                        t.save()
            if not current_package.has_next:
                role = request.user.role
                if role == "expert":
                    current_package.is_tagged = True
                elif role == "full_expert":
                    current_package.is_valid = True
                current_package.status = "available"
                current_package.save()
        except Exception as e:
            print(str(e))
        return super(UserOutputAPIView, self).post(request, *args, **kwargs)


class PackageProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePackageSerializer
    queryset = ProfilePackage.objects.all()

    def get_object(self):
        role = self.request.user.role
        package = ProfilePackage.objects \
            .filter(process__id=self.kwargs['pid'], status="available", is_tagged=(role == "full_expert")) \
            .order_by('id') \
            .first()
        if package is not None:
            package.status = "blocked"
            millis = int(round(time.time() * 1000))
            package.expire_date = str(millis + 1*60*60*1000)  # set expire date to 1 hour after getting package
            package.save()
            return package
        else:
            raise Http404
