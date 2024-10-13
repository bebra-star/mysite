from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, first_language, second_language):
        user = self.model(
            username=username,
            first_language=first_language,
            second_language=second_language,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
