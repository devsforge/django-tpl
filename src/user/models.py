"""
Custom user model

.. seealso::
    https://docs.djangoproject.com/en/dev/topics/auth/customizing/
    https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#substituting-a-custom-user-model
    https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#referencing-the-user-model

"""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
