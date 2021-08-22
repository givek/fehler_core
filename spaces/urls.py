from django.urls import path

from . import views


urlpatterns = [
    # path('spaces/<int:user_id>', views.space_list_view, name='space_list'),
    path("spaces/<int:user_id>", views.SpaceListView.as_view(), name="space_list"),
]
