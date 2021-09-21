from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import SpaceSerializer
from .models import SpaceMembership


class ListSpaces(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """
        Return a list of all spaces a particular user is associated with.
        """
        space_memberships = SpaceMembership.objects.filter(user=user_id)
        user_spaces = [
            {"id": space_membership.space_id, "name": space_membership.space.name}
            for space_membership in space_memberships
        ]
        return Response(user_spaces, status=status.HTTP_200_OK)


class CreateSpace(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new space with provided credentials.
        """
        space_serializer = SpaceSerializer(data=request.data)
        if space_serializer.is_valid(raise_exception=True):
            new_space = space_serializer.save()
            if new_space:
                space_memberships = SpaceMembership.objects.filter(
                    user=request.data["owner"]
                )
                user_spaces = [
                    {
                        "id": space_membership.space_id,
                        "name": space_membership.space.name,
                    }
                    for space_membership in space_memberships
                ]
                return Response(user_spaces, status=status.HTTP_200_OK)
        return Response(space_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
