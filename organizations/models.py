from django.db import models
from django.conf import settings
# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name


class OrganizationMember(models.Model):


    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MEMBER = 'MEMBER', 'Member',
        OWNER = 'OWNER', 'Owner'


    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_memberships')

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    joined_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'user'], name='unique_organization_member')
        ]