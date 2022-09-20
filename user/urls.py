from django.urls import path, re_path

from . import views
from .autocomplete_views import UserAutocomplete

app_name = "user"

urlpatterns = [

    path("~redirect/", view=views.UserRedirectView.as_view(),
         name="redirect"),
    path("~update/", view=views.UserUpdateView.as_view(),
         name="update"),
    path("user/<str:username>/", view=views.UserDetailView.as_view(),
         name="detail"),
    path("user-autocomplete/",
         UserAutocomplete.as_view(),
         name='user-autocomplete'),
    re_path(r'^profile/', views.UserProfile.as_view(),
         name='profile'),
]
