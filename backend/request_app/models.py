from django.db import models

from auth_app.models import User
from tags.models import Tag


class Requests(models.Model):
    CHOICES = (
        ('accepted', "Принято"),
        ('in_process', "В процессе"),
        ('declined', 'Отклонено')
    )

    mentor = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="ment")
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="stud")
    tags = models.ManyToManyField(to=Tag)
    problem = models.CharField(max_length=1024, null=True)
    status = models.CharField(max_length=20, choices=CHOICES)
