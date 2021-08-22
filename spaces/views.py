from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from .models import Space, Membership
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

# @api_view(('GET',))
# def space_list_view(request, user_id):
#     print(user_id)
#     space_list = Space.objects.get(owner=user_id)
#     return Response({'space_list': space_list.name}, status=status.HTTP_200_OK)


class SpaceListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        print(user_id)
        space_list = Membership.objects.filter(user=user_id)
        print(space_list)
        return Response({"space_list": space_list}, status=status.HTTP_200_OK)
