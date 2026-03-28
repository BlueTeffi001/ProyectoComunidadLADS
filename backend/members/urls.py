from django.urls import path
from .views import members_list

urlpatterns = [
    path("members/", members_list, name="members-list"),
]