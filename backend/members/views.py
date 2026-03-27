from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    profile = request.user.memberprofile

    if profile.status != "approved":
        return render(request, "members/not_approved.html")

    return render(request, "members/profile.html")