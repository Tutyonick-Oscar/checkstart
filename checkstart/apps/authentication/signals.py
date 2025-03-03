from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from checkstart.apps.core.utils.main import delete_related_objects


@receiver(pre_delete, sender=get_user_model())
def delete_user_related_objects(sender, instance, **kwargs):
    print("deleting : ", instance)
    try:
        delete_related_objects(instance=instance)
    except Exception as e:
        print("Can't delete related objects : ", str(e))
