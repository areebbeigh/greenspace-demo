import sys

from django.conf import settings

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    group, created = Group.objects.get_or_create(name=settings.NURSERY_MGR_GROUP)
    print('Created new nursery group' if created else 'Nursery group already exists')
