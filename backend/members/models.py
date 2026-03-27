from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class MemberProfile(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("approved", "Aprobado"),
        ("rejected", "Rechazado"),
    ]

    ROLE_CHOICES = [
        ("member", "Miembro"),
        ("moderator", "Moderador"),
        ("editor", "Editor"),
        ("admin", "Admin"),
    ]

    MAIN_CHOICES = [
        ("xavier", "Xavier"),
        ("sylus", "Sylus"),
        ("zayne", "Zayne"),
        ("rafayel", "Rafayel"),
        ("caleb", "Caleb"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_li = models.CharField(max_length=20, choices=MAIN_CHOICES, default="xavier")
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    can_edit_profile = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_member_profile(sender, instance, **kwargs):
    MemberProfile.objects.get_or_create(user=instance)
    instance.memberprofile.save()