from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Requests
from .swagger import rq_body_scheme, rs_success, not_found
from .serializers import RequestSerializer


class RequestViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def _manage_reqs(self, request, pk, status):
        user = request.user
        reqs = Requests.objects.filter(Q(mentor=user) | Q(student=user), id=pk)
        if not reqs.exists():
            return Response({
                "message": "req not found"
            }, status=404)

        req = reqs.first()
        req.status = status
        req.save()

        return Response({
            "message": RequestSerializer(reqs, many=True).data
        })

    @swagger_auto_schema(
        request_body=rq_body_scheme,
        responses={
            200: rs_success,
            400: not_found
        }
    )
    def create(self, request):
        serializer = RequestSerializer(data=request.data, context={"student": request.user})
        serializer.is_valid(raise_exception=True)

        try:
            req = serializer.save()
        except ValidationError as e:
            return Response({
                "message": e.detail
            }, status=404)
        return Response(RequestSerializer(req).data, status=201)

    @swagger_auto_schema(
        responses={
            200: rs_success,
            400: not_found
        }
    )
    def retrieve(self, request, pk):
        user = request.user
        reqs = Requests.objects.filter(Q(mentor=user) | Q(student=user), id=pk)
        if not reqs.exists():
            return Response({
                "message": "req not found"
            }, status=404)
        return Response(RequestSerializer(reqs.first()).data)

    @swagger_auto_schema(
        responses={
            200: RequestSerializer(many=True)
        }
    )
    def list(self, request):
        user = request.user
        reqs = Requests.objects.filter(Q(mentor=user) | Q(student=user))
        return Response(RequestSerializer(reqs, many=True).data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Request accepted', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                }
            )),
            404: openapi.Response('Request not found', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    )
    @action(methods=['post'], detail=True)
    def accept(self, request, pk):
        response = self._manage_reqs(request, pk, "accepted")
        if response.status_code == 404:
            return response

        req = Requests.objects.get(id=pk)
        if request.user == req.student:
            tg_username = req.mentor.tg
        else:
            tg_username = req.student.tg

        return Response({
            "message": RequestSerializer(req).data,
            "tg_username": tg_username
        })

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Request declined', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                }
            )),
            404: openapi.Response('Request not found', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    )
    @action(methods=['post'], detail=True)
    def decline(self, request, pk):
        return self._manage_reqs(request, pk, "declined")
