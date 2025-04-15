import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import jwt

from tags.models import Tag
from .managers import UserManager
from tags.models import Tag


class User(AbstractBaseUser, PermissionsMixin):
    CHOICES = (
        ("admin", "Админ"),
        ("mentor", "Ментор"),
        ("student", "Студент")
    )

    login = models.CharField(max_length=128, verbose_name="Login", unique=True)
    fio = models.CharField(max_length=50)
    tg = models.CharField(verbose_name="TG username", unique=True, max_length=256)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(verbose_name="Роль", choices=CHOICES, max_length=20)
    course = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6)
        ]
    )
    description = models.TextField(null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='')
    tags = []
    
    EMAIL_FIELD = "tg"
    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["tg"]

    objects = UserManager()

    def __str__(self):
        return self.login

    def get_username(self):
        return self.login
    
    @property
    def token(self):
        return self._generate_token_jwt()
    
    def _generate_token_jwt(self):
        dt = timezone.now() + datetime.timedelta(days=36)

        return jwt.encode(
            {
                "id": self.id,
                "exp": int(dt.timestamp())
            },
            settings.SECRET_KEY,
        )


class MentorProfile(models.Model):
    mentor_rating = models.FloatField(default=0.0)
    mentor = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="mentor")
    students = models.ManyToManyField(to=User)
    tags = models.ManyToManyField(to=Tag)
    rating_sum = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    
    def update_rating(self, rating: int):
        self.rating_sum += rating
        self.rating_count += 1
        self.mentor_rating = self.rating_sum / self.rating_count
        self.save()


class StudentProfile(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="student")
