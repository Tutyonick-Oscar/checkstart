import auto_prefetch
from django.db import models
from django.utils import timezone

from checkstart.apps.core.middlewares import local
from checkstart.settings.settings import AUTH_USER_MODEL


class CustomQueryset(auto_prefetch.QuerySet):

    def delete(self):
        return self.update(deleted_at=timezone.now())


class BaseManager(auto_prefetch.Manager):

    def get_queryset(self) -> models.QuerySet:
        return CustomQueryset(model=self.model, using=self._db).filter(deleted_at=None)


class BaseModel(auto_prefetch.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = auto_prefetch.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name="%(class)ss"
    )
    deleted_at = models.DateTimeField(blank=True, default=None, null=True)

    objects = BaseManager()

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        base_manager_name = "prefetch_manager"
        default_manager_name = "objects"

    def delete(self, **kwargs):

        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        self.deleted_at = timezone.now()
        self.save(force=True)
        return self

    def save(self, force=False, *args, **kwargs):
        if force:
            return super().save(*args, **kwargs)

        if self.pk is None:
            auth_user = getattr(local, "CURRENT_USER", None)
            if auth_user:
                self.created_by = auth_user
                return super().save(*args, **kwargs)

            return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)
