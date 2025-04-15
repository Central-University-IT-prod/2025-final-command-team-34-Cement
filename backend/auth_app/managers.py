from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, login, tg, password = None, **kwargs):
        user = self.model(login=login, tg=self.normalize_email(tg), **kwargs)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, login, tg, password):
        user = self.create_user(login, tg, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
