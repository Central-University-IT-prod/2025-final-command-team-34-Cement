from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_app.models import User, MentorProfile
from auth_app.serializers import UserSerializer
from django.conf import settings
import requests


class SearchAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "tag",
                openapi.IN_QUERY,
                description="ID тега, их может быть несколько, например ?tag=1&tag=2&tag=3",
                type=openapi.TYPE_INTEGER,
                required=False,
                collectionFormat="multi",
            ),
            openapi.Parameter(
                "problem",
                openapi.IN_QUERY,
                description="Если пользователь использует ai-filter, то передать его проблему в этот параметр",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of mentors",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "login": openapi.Schema(type=openapi.TYPE_STRING),
                            "tg": openapi.Schema(type=openapi.TYPE_STRING),
                            "description": openapi.Schema(type=openapi.TYPE_STRING),
                            "course": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "role": openapi.Schema(type=openapi.TYPE_STRING),
                            "fio": openapi.Schema(type=openapi.TYPE_STRING),
                            "mentor_rating": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "tags": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                        "name": openapi.Schema(
                                            type=openapi.TYPE_STRING
                                        ),
                                    },
                                ),
                            ),
                            "profile_image": openapi.Schema(type=openapi.TYPE_STRING, description="Url фото"),
                            "ai_score": openapi.Schema(
                                type=openapi.TYPE_NUMBER,
                                description="чем больше число, тем больше ментор подходит пользователю, передается только если в параметрах была передана проблема",
                                example=0.6,
                            ),
                        },
                    ),
                ),
            )
        },
    )
    def get(self, request):
        query_params = request.query_params
        mentor_profiles = MentorProfile.objects.all()
        mentors = []

        tags = query_params.getlist("tag")
        problem = query_params.get("problem")
        if tags:
            for tag in tags:
                mentor_profiles = mentor_profiles.filter(tags__id=tag)

        for mp in mentor_profiles:
            mentors.append(UserSerializer(mp.mentor).data)
        if problem:
            for mentor in mentors:
                response = requests.post(
                    f"http://{settings.AI_FILTER_BASE_URL}/predict/single",
                    json={"texts": [problem, mentor["description"]]},
                )
                mentor["ml_score"] = float(response.text)
        return Response(mentors)
