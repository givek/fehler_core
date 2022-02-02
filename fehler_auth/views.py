from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterUserSerializer, InviteSerializer, AuthTokenSerializer
from .models import User, Invite
from .forms import UserInviteForm, UserInviteRegisterForm
from .utils import token_generator

from spaces.models import Space, SpaceMembership


class UserDetails(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Return details of current authenticated user.
        """
        token = request.data["token"]
        user = Token.objects.get(key=token).user
        if user:
            user_data = {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            }
            return Response(user_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid(raise_exception=True):
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InviteUserApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        invite_serializer = InviteSerializer(data=request.data)
        if invite_serializer.is_valid():
            new_invite = invite_serializer.save()
            user_email = request.data["email"]
            created = self.create_unusbale_user(user_email)
            if created:
                domain = get_current_site(request).domain
                self.send_invite(new_invite, user_email, domain, request.data["space"])

            if new_invite:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)  # send errors

    def create_unusbale_user(self, email):
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.save()
            return True
        return False

    def send_invite(self, invite, user_email, domain, space_id):
        user = User.objects.get(email=user_email)
        activation_link = invite.get_absolute_url(user, space_id, domain)
        invite.email_invite(activation_link)
        print(invite.email_invite(activation_link))


class VerificationView(View):
    model = User
    slug_field = "name"
    form_class = UserInviteRegisterForm
    template_name = "fehler_auth/register.html"

    def get(self, request, space_id, uid64, token):

        user = self.decode_user(uid64)
        if not token_generator.check_token(user, token):
            # return redirect('login')
            return HttpResponseNotFound("<h1>token check invalid</h1>")

        invite = get_object_or_404(Invite, email=user.email)
        if not invite.is_valid():
            return HttpResponseNotFound("<h1>invite not found</h1>")

        self.create_space_membership(user, invite, space_id)

        # data = {'email': user.email}
        form = self.form_class()

        return render(request, self.template_name, {"form": form})

    def post(self, request, space_id, uid64, token):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=False)
            password = form.cleaned_data["password"]

            user = self.decode_user(uid64)
            user.set_password(password)
            user.save()

            return redirect("http://localhost:3000/login")

        return render(request, self.template_name, {"form": form})

    def create_space_membership(self, user, invite, space_id):
        space = Space.objects.get(id=space_id)
        # invite = Invite.objects.get(email=user.email)
        member = SpaceMembership.objects.create(
            member=user, space=space, invite=invite, type_of_member=invite.member_type
        )
        member.save()

    def decode_user(self, uid64):
        uid = force_text(urlsafe_base64_decode(uid64))
        user = get_object_or_404(User, pk=uid)
        return user
