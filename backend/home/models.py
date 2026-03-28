from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect, render
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class HomePage(Page):
    is_exclusive = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("is_exclusive"),
    ]

    def serve(self, request):
        if self.is_exclusive:
            if not request.user.is_authenticated:
                return redirect("/admin/login/?next=/")

            profile = request.user.memberprofile
            if profile.status != "approved":
                return render(request, "members/not_approved.html")

        return super().serve(request)


class Comment(models.Model):
    page = models.ForeignKey(
        HomePage, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
