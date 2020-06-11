from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    def __str__(self):
        return f'User<{self.username}>'

    def is_nursery_manager(self):
        return self.groups.filter(name=settings.NURSERY_MGR_GROUP).exists()