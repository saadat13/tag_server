from django.db.models import Q
from django.http import JsonResponse, Http404, HttpResponse
from rest_framework.generics import ListAPIView
from django.shortcuts import get_list_or_404

from accounts.models import CustomUser
from .pagination import PostPageNumberPagination
from .models import Process, UserOutput, Tag, Profile, OutputTag
from .serializers import ProcessSerializer, UserOutputSerializer, \
    ProfileSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import asyncio
import json


class ProcessListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = ProcessSerializer
    queryset = Process.objects.filter(is_valid=False).all()
    # pagination_class = PostPageNumberPagination
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        query = []
        if str(user) != "AnonymousUser":
            role = user.role
            if role == "full_expert":
                query = self.queryset.filter(status="available", is_tagged=True) | \
                        self.queryset.filter(full_expert_user=user)
            elif role == "expert":
                query = self.queryset.filter(status="available", is_tagged=False) | \
                        self.queryset.filter(expert_user=user, is_tagged=False)
        return get_list_or_404(query)


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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(handle_output(request))


async def handle_output(request):
    response_code = 400
    data = json.loads(request.data)
    process_id = int(data[0]['process_id'])
    current_process = Process.objects.filter(pk=process_id)
    if current_process:
        current_process = current_process.first()
        user = request.user
        if str(user) != "AnonymousUser":
            for item in data:
                profile_id = item['profile_id']
                user_output = UserOutput.objects.create(process_id=process_id, profile_id=profile_id)
                for t in item['tags']:
                    output_tag = OutputTag.objects.create(title=t['title'], user_output=user_output)

            role = user.role
            if role == "expert":
                current_process.expert_user = user
                if current_process.profile_set.filter(is_tagged=False).count() == 1:
                    current_process.profile_set.filter(is_tagged=True).update(is_tagged=False)
                    current_process.status = "available"
                    current_process.is_tagged = True
                else:
                    for item in data:
                        profile_id = item['profile_id']
                        current_process.profile_set.filter(id=profile_id).update(is_tagged=True)
                for item in data:
                    profile_id = item['profile_id']
                    for t in item['tags']:
                        p = Profile.objects.filter(pk=profile_id)
                        if p:
                            Tag.objects \
                                .filter(process__id=process_id, title=t['title']) \
                                .update(profile=p.first())
                response_code = 200
            elif role == "full_expert":
                current_process.full_expert_user = user
                if current_process.profile_set.filter(is_tagged=False).count() == 1:
                    current_process.is_valid = True
                for item in data:
                    profile_id = item['profile_id']
                    current_process.profile_set.filter(id=profile_id).update(is_tagged=True)
                response_code = 200
            current_process.save()
    return JsonResponse({'error':'response'},status=response_code)


class ProfileListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # pagination_class = PostPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if str(user) != "AnonymousUser":
            role = user.role
            current_process = Process.objects.filter(pk=self.kwargs['pk'])
            if current_process:
                current_process = current_process.first()
                if role == "expert":
                    current_process.expert_user = user
                elif role == "full_expert":
                    current_process.full_expert_user = user
                current_process.status = "blocked"
                current_process.save()
                query_set = current_process.profile_set.filter(is_tagged=False)
                return get_list_or_404(query_set)
            raise Http404("no process exists")
        raise Http404("anonymous user")

