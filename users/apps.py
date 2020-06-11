from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from .signals import create_groups
        post_migrate.connect(create_groups, sender=self)
