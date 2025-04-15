from functools import wraps

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


rq_body_scheme = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "mentor": openapi.Schema(type=openapi.TYPE_INTEGER),
        "tags": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_INTEGER),
        ),
        "problem": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "status": openapi.Schema(
            type=openapi.TYPE_STRING,
            enum=["accepted", "in_process", "declined"],
        ),
    },
    required=["student_id", "mentor_id"],
)

rs_success = openapi.Response(
    "Request created",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "student": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "login": openapi.Schema(type=openapi.TYPE_STRING),
                    "tg": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "course": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "role": openapi.Schema(type=openapi.TYPE_STRING),
                    "fio": openapi.Schema(type=openapi.TYPE_STRING),
                    "profile_image": openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                },
            ),
            "mentor": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "login": openapi.Schema(type=openapi.TYPE_STRING),
                    "tg": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "course": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "role": openapi.Schema(type=openapi.TYPE_STRING),
                    "fio": openapi.Schema(type=openapi.TYPE_STRING),
                    "profile_image": openapi.Schema(
                        type=openapi.TYPE_STRING
                    ),
                    "mentor_rating": openapi.Schema(
                        type=openapi.TYPE_NUMBER
                    ),
                    "tags": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_STRING),
                    ),
                },
            ),
            "tags": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
            ),
            "problem": openapi.Schema(
                type=openapi.TYPE_STRING, nullable=True
            ),
            "status": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)

not_found = openapi.Response(
    "Validation error",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
    ),
)

