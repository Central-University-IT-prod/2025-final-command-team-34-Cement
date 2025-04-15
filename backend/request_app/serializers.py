from rest_framework import serializers
from rest_framework import exceptions

from auth_app.models import User
from tags.models import Tag
from auth_app.serializers import UserSerializer
from .models import Requests


class RequestSerializer(serializers.ModelSerializer):
    mentor = serializers.IntegerField()
    student = serializers.IntegerField(read_only=True)
    tags = serializers.ListField()
    status = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Requests
        fields = ("mentor", "student", "tags", "problem", "status")


    def create(self, validated_data):
        mentor = User.objects.filter(role = "mentor").filter(id=validated_data['mentor'])
        print(self.context)
        student = User.objects.filter(role = "student").filter(id=self.context['student'].id)
        if not mentor.exists() or not student.exists():
            raise exceptions.ValidationError("Mentor or student must be specified")
        mentor, student = mentor.first(), student.first()
        validated_data['mentor'] = mentor
        validated_data['student'] = student
        filter_tags = []

        for tag_id in validated_data['tags']:
            tag = Tag.objects.filter(id=tag_id)
            if not tag.exists():
                raise exceptions.ValidationError(f"Tag with id {tag_id} not found")
            filter_tags.append(
                tag.first()
            )

        del validated_data['tags']
        if "status" not in validated_data:
            validated_data["status"] = "in_process"
        requests = Requests.objects.create(**validated_data)

        for tag in filter_tags:
            requests.tags.add(tag)
        
        return requests
    
    def to_representation(self, instance: Requests):
        return {
            "id": instance.id,
            "student": UserSerializer(instance.student).data,
            "mentor": UserSerializer(instance.mentor).data,
            "tags": [tag.name for tag in instance.tags.all()],
            "tags_ids": [tag.id for tag in instance.tags.all()],
            "problem": instance.problem,
            "status": instance.status
        }
        
