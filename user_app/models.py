from django.db import models
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

# Create your models here.
#we will use deafult django user model so no need to do or override anything here for our requirements
#creates token automatically when user is created
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)