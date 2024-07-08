from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Por favor ingresa un Email Valido"))


    def create_user(self, username, email, name, last_name, password, profession, image_face, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)

        
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            profession = profession,
            image_face = image_face,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, last_name, password,**extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser",  True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("profession", "Administrador")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is_staff tiene que ser verdadero para el usuario administrador"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is_superuser tiene que ser verdadero para el usuario administrador"))
        
        if extra_fields.get("profession") != "Administrador":
            raise ValueError(_("profession tiene que ser -Administrador- para el usuario administrador"))

        user = self.create_user(username, email, name, last_name, password, **extra_fields)
        user.save(using=self._db)
        return user