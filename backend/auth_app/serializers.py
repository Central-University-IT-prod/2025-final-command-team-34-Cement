from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.validators import ValidationError

from tags.models import Tag
from .models import User, MentorProfile, StudentProfile


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        allow_blank = False,
        write_only = True
    )
    tags = serializers.ListField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ('login', 'tg', 'password', 'description', 'course', 'role', 'token', 'fio', 'tags', 'profile_image')
    
    def create(self, validated_data):
        tags = validated_data.get('tags')
        if tags is not None:
            del validated_data['tags']
        user: User = User.objects.create_user(**validated_data)

        if user.role == "mentor":
            tags = tags if tags else []
            profile = MentorProfile.objects.create(mentor=user)
            new_tags = []
            for tag_id in tags:
                tag = Tag.objects.filter(id=tag_id)
                if tag.exists():
                    profile.tags.add(tag.first())
                    new_tags.append(tag_id)
            setattr(user, "tags", new_tags)
        if user.role == "student":
            StudentProfile.objects.create(student=user)
        return user


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs: dict):
        login =  attrs.get('login')
        password = attrs.get('password')

        if not login or not password:
            raise serializers.ValidationError("login or password weren't specified")
        
        return {
            "login": login,
            "password": password
        }

    def authentication(self):
        user: User = authenticate(login=self.validated_data["login"], password=self.validated_data["password"])

        if user is None:
            raise exceptions.AuthenticationFailed("Wrong auth credentials")

        return user.token, user.role


class MentorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProfile
        fields = ('mentor_rating',)

    def to_representation(self, instance):
        data: dict = super().to_representation(instance)
        
        data['tags'] = list(instance.tags.values())
        
        return data


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'login', 'tg', 'description', 'course', 'role', 'fio', 'profile_image')

    def update(self, instance: User, validated_data: dict):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        
        instance.save()

        return instance

    def to_representation(self, instance: User):
        data: dict = super().to_representation(instance)

        if instance.role == "student":
            student_profile = StudentProfile.objects.get(student=instance)
            data.update(StudentProfileSerializer(student_profile).data)
            # del data['tags']
        if instance.role == "mentor":
            mentor_profile = MentorProfile.objects.get(mentor=instance)
            data = {
                **data,
                **MentorProfileSerializer(mentor_profile).data
            }
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs: dict):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        user: User = self.context.get("user")

        if not old_password or not new_password:
            raise serializers.ValidationError("old_password or new_password weren't specified")
        
        is_ok = user.check_password(old_password)

        if not is_ok:
            raise serializers.ValidationError(
                "old password is wrong!"
            )
        
        return {
            "new_password": new_password
        }
    
    def save(self):
        user: User = self.context.get("user")
        user.set_password(self.validated_data["new_password"])
        user.save()

        return user


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
