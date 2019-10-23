from django.http import JsonResponse, Http404
from rest_framework.generics import ListAPIView
from django.shortcuts import get_list_or_404

from accounts.models import CustomUser
from .pagination import PostPageNumberPagination
from .models import Process, UserOutput, Tag, Profile
from .serializers import ProcessSerializer, UserOutputSerializer, \
    ProfileSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class ProcessListAPIView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = ProcessSerializer
    queryset = Process.objects.all()
    # pagination_class = PostPageNumberPagination
    lookup_field = 'pk'

    # TODO may be uncommented
    def get_queryset(self):
        # TODO uncomment this
        user = self.request.user
        if str(user) != "AnonymousUser":
            role = user.role
            if role == "full_expert":
                return get_list_or_404(Process.objects.filter(is_tagged=True).all())
            elif role == "expert":
                return get_list_or_404(Process.objects.filter(status="available").all())
        return []


class ProcessAPIView(generics.RetrieveAPIView):
    serializer_class = ProcessSerializer
    queryset = Process.objects.filter(status="available").all()
    lookup_field = 'pk'


class UserOutputAPIView(ListAPIView, generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = UserOutputSerializer
    queryset = UserOutput.objects.all()
    # pagination_class = PostPageNumberPagination

    def post(self, request, *args, **kwargs):
        data = request.data
        process_id = int(data['process_id'])
        current_process = Process.objects.filter(pk=process_id)
        if current_process:
            current_process = current_process.first()
            user = request.user
            if str(user) != "AnonymousUser":
                role = user.role
                if role == "expert":
                    current_process.is_tagged = True
                    for t in data['tags']:
                        Tag.objects.filter(process__id=process_id, title=t['title']).update(is_checked=True)
                elif role == "full_expert":
                    current_process.is_valid = True
                current_process.save()
        return super(UserOutputAPIView, self).post(request)


class ProfileListAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # pagination_class = PostPageNumberPagination

    def get_queryset(self):
        try:
            current_process = Process.objects.get(pk=self.kwargs['pk'])
            if current_process.status == "available":
                current_process.status = "blocked"
                current_process.save()
            query_set = current_process.profile_set.all()
            return get_list_or_404(query_set)
        except Exception as e:
            raise Http404("No model matches the given query.")
