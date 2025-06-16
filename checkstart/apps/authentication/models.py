from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from checkstart.apps.core.models import BaseManager, BaseModel
from checkstart.apps.core.validators.name import str_checker
from checkstart.apps.core.validators.password import (
    lowercase_checker,
    name_in_password_checker,
    number_checker,
    special_characters_checker,
    uppercase_checker,
)


class UserManager(BaseUserManager, BaseManager):

    def create_user(self, email, password, username, **kwargs):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, **kwargs):
        user = self.create_user(email, password, username, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(BaseModel, AbstractBaseUser):
    created_by = None
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, validators=[str_checker])
    password = models.CharField(
        ("password"),
        max_length=128,
        validators=[
            MinLengthValidator(8),
            special_characters_checker,
            uppercase_checker,
            lowercase_checker,
            number_checker,
        ],
    )
    photo = models.ImageField(upload_to="users_profil_photos/", null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username"]

    def __str__(self) -> str:
        return self.username

    objects = UserManager()

    def has_perms(self, perms, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def clean(self):
        super().clean()
        name_in_password_checker(self.password, self.username)

    class Meta(BaseModel.Meta):
        default_manager_name = "objects"
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=[
        #         ],  # USERNAME_FIELD must not be included here,
        #         condition=models.Q(deleted_at=None),
        #         name="unique_undeleted_user",
        #         violation_error_message="phone number or device address already in use",
        #     )
        # ]
        indexes = [
            models.Index(
                fields=("deleted_at",),
                name="indexing_undeleted_users",
                condition=models.Q(deleted_at=None),
            )
        ]

    # for USERNAME_FIELD unique constraint purpose
    def delete(self, **kwargs):
        self.email = self.email + f"_deleted_at_{timezone.now()}"
        return super().delete(**kwargs)
