import datetime

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
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from pytz import utc

from . serializers import RegisterUserSerializer
from . models import User, Invite
from . forms import UserInviteForm, UserInviteRegisterForm
from . utils import token_generator


class TestAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_201_CREATED)

        
class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInvite(View):
    model = User
    slug_field = "name"
    form_class = UserInviteForm
    template_name = 'fehler_auth/invite.html'

    def get(self, request):
        form = self.form_class()
        # data = {'org_name': slug}
        # form = self.form_class(initial=data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            # invite.organistion = Organistion.objects.get(id=org_pk)
            invite.save()
            
            email = form.cleaned_data['email']
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.set_unusable_password()
                user.save()
            
            domain = get_current_site(request).domain
            # activation_link = invite.get_absolute_url(user, org, domain)
            activation_link = invite.get_absolute_url(user, domain)
            
            invite.email_invite(activation_link)
            return redirect('invite')

        return render(request, self.template_name, {'form': form})


class VerificationView(View):
    model = User
    slug_field = "name"
    form_class = UserInviteRegisterForm
    template_name = 'fehler_auth/register.html'

    def get(self, request, uid64, token):

        uid = force_text(urlsafe_base64_decode(uid64))
        user = get_object_or_404(User, pk=uid)

        if not token_generator.check_token(user, token):
            # return redirect('login')
            return HttpResponseNotFound('<h1>token check invalid</h1>')
        
        invite = get_object_or_404(Invite, email=user.email)
        if invite.is_valid() == False:
            return HttpResponseNotFound('<h1>invite not found</h1>')
        
        # org = Organistion.objects.get(id=org)
        invite = Invite.objects.get(email=user.email)
        # member = Membership.objects.create(user=user, organisation=org, invite=invite)
        # member.save()
        
        # data = {'email': user.email}
        form = self.form_class()
        
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, uid64, token):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=False)
            password = form.cleaned_data['password']
            
            uid = force_text(urlsafe_base64_decode(uid64))
            user = get_object_or_404(User, pk=uid)
            user.set_password(password)
            user.save()

            return redirect('invite')

        return render(request, self.template_name, {'form': form})



