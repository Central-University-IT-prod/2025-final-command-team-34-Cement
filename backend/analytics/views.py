from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from tags.models import Tag
from request_app.models import Requests
from auth_app.models import MentorProfile, StudentProfile


class AnalyticsViewSet(ViewSet):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Статистика по тегам менторов",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название тега'),
                            'mentors': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество менторов с этим тегом'),
                            'id': openapi.Schema(type=openapi.TYPE_STRING, description='Id токена')
                        }
                    )
                )
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='mentors/tags/')
    def get_tag_stats(self, request):
        tag_stats = dict()
        ids = dict()
        for mentor in MentorProfile.objects.all():
            for tag in mentor.tags.all():
                name = tag.name
                if name in tag_stats:
                    tag_stats[name] = tag_stats[name] + 1
                else:
                    tag_stats[name] = 1
                ids[name] = tag.id
        for tag in Tag.objects.all():
            if tag.name not in tag_stats:
                tag_stats[tag.name] = 0
                ids[tag.name] = tag.id
        sorted_tags = sorted(tag_stats.items(), key=lambda x: x[1], reverse=True)[:7]

        res = [{"id": ids[t[0]],"name": t[0], "mentors": t[1]} for t in sorted_tags]

        return Response(res)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Количество менторов и студентов",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'mentors': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество менторов'),
                        'students': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество студентов'),
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='count/')
    def get_count(self, request):
        return Response({"mentors": MentorProfile.objects.count(), "students": StudentProfile.objects.count()})

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Топ менторов по рейтингу",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Логин ментора'),
                            'value': openapi.Schema(type=openapi.TYPE_NUMBER, description='Рейтинг ментора'),
                            'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество оценок')
                        }
                    )
                )
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='mentors/stats/')
    def get_top_mentors(self, request):
        result = [
            {"name": x.mentor.login, "value": x.mentor_rating, "count": x.rating_count}
            for x in MentorProfile.objects.order_by('-mentor_rating')[:10]
        ]
        return Response(result)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Статистика по запросам",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'declined': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество отклоненных заявок'),
                            'accepted': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество принятых заявок'),
                            'ignored': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество не прочитанных заявок'),
                        }
                    )
                )
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='requests/stats/')
    def get_requests_stats(self, request):
        result = {
            "declined": Requests.objects.filter(status = "declined").count(),
            "accepted": Requests.objects.filter(status = "accepted").count(),
            "ignored": Requests.objects.filter(status = "in_process").count()
        }
        return Response(result)
