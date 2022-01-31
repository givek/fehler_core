from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from fehler_auth.models import User

from .serializers import SpaceSerializer
from .models import SpaceMembership
from .models import Space


class ListSpaces(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """
        Return a list of all spaces a particular user is associated with.
        """
        space_memberships = SpaceMembership.objects.filter(member=user_id)
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
                owner_email = request.data["owner"]
                owner = User.objects.get(email=owner_email)
                member = self.create_space_membership(owner, new_space.id)
                space_memberships = SpaceMembership.objects.filter(member=owner)
                user_spaces = [
                    {
                        "id": space_membership.space_id,
                        "name": space_membership.space.name,
                    }
                    for space_membership in space_memberships
                ]
                return Response(user_spaces, status=status.HTTP_200_OK)
        return Response(space_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_space_membership(self, user, space_id):
        space = Space.objects.get(id=space_id)
        # invite = Invite.objects.get(email=user.email)
        member = SpaceMembership.objects.create(
            member=user, space=space, type_of_member="Owner"
        )
        member.save()


class DeleteSpace(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, space_id):
        """
        Delete a space with provided credentials.
        """
        space = Space.objects.get(id=space_id)
        space.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
