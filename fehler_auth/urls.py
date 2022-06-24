from django.urls import path

from .views import (
    CustomObtainAuthToken,
    RegisterUser,
    InviteUserApi,
    VerificationView,
    UserDetails,
)


urlpatterns = [
    path("register/", RegisterUser.as_view(), name="create_user"),
    path("token/", CustomObtainAuthToken.as_view(), name="token_obtain"),
    # path('<space_id>/invite/', views.UserInvite.as_view(), name='invite'),
    path("spaces/<str:space_name>/invite/", InviteUserApi.as_view(), name="inviteapi"),
    path(
        "<space_id>/activate/<uid64>/<token>/",
        VerificationView.as_view(),
        name="activate",
    ),
    path("user-details/", UserDetails.as_view(), name="user_details"),
]
