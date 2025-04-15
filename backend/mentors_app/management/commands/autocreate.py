from random import random

from django.core.management.base import BaseCommand

from ._data import tags, mentors, students, admin, requests
from auth_app.models import User, MentorProfile
from auth_app.serializers import RegistrationSerializer, StudentProfileSerializer
from request_app.serializers import RequestSerializer
from tags.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        global admin

        for tag in tags:
            Tag.objects.create(**tag)

        for student in students:
            student["password"] = "1"
            serializer = RegistrationSerializer(data=student)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(student)

        print("students generation started...")

        admin['password'] = '1'
        admin = RegistrationSerializer(data=admin)
        admin.is_valid(raise_exception=True)
        admin.save()

        for mentor in mentors:
            mentor['password'] = '1'
            serializer = RegistrationSerializer(data=mentor)
            serializer.is_valid(raise_exception=True)
            ment = serializer.save()
            mentor_profile = MentorProfile.objects.get(mentor=ment)
            mentor_profile.mentor_rating = random()*5
            mentor_profile.save()
            print(mentor)

        print("mentors generation started...")

        for request in requests:
            request['mentor'] = request['mentor'] + 51
            print(request)
            user = User.objects.filter(role="student").filter(id=request['student']).first()
            print(RegistrationSerializer(user).data)
            serializer = RequestSerializer(data=request, context={"student": user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(request)

        ratings = [3.1, 4.2, 5.0, 4.3, 4.8, 3.2, 4.9]
        counts = [15, 7, 1, 9, 21, 4, 19]
        i = 0
        for mentor in MentorProfile.objects.all():
            mentor.rating_count = counts[i % len(ratings)]
            mentor.rating_sum = ratings[i % len(ratings)] * counts[i % len(ratings)]
            mentor.mentor_rating = ratings[i % len(ratings)]
            i += 1
            mentor.save()

        print("requests generation started...")

        print("Data generation ended...")
