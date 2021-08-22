from django.urls import path

from . import views


urlpatterns = [
    path("register", views.RegisterUser.as_view(), name="create_user"),
    path("token", views.ObtainExpiringAuthToken.as_view(), name="token_obtain"),
    # path('<space_id>/invite/', views.UserInvite.as_view(), name='invite'),
    path("invite/", views.InviteUserApi.as_view(), name="inviteapi"),
    path(
        "<space_id>/activate/<uid64>/<token>",
        views.VerificationView.as_view(),
        name="activate",
    ),
]
