from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializer import TagSerializer, Tag


class TagViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=TagSerializer,
        responses={
            201: TagSerializer(),
            400: openapi.Response('Validation error', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    )
    def create(self, request):
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

    @swagger_auto_schema(
        responses={
            200: TagSerializer(),
            400: openapi.Response('Tag not found', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    )
    def retrieve(self, request, pk):
        tag = Tag.objects.filter(id=pk)
        if not tag.exists():
            return Response({
                "message": "Tag not found"
            }, status=400)

        return Response(
            TagSerializer(tag.first()).data,
        )

    @swagger_auto_schema(
        request_body=TagSerializer(many=True),
        responses={
            201: TagSerializer(many=True),
            400: openapi.Response('Validation error', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    )
    @action(methods=["post"], detail=False)
    def bulk(self, request):
        tags = TagSerializer(data=request.data, many=True)
        tags.is_valid(raise_exception=True)

        created_tags = []

        for tag in tags.data:
            serializer = TagSerializer(data=tag)
            serializer.is_valid()
            serializer.save()
            created_tags.append(serializer.data)

        return Response(created_tags, status=201)
    
    @swagger_auto_schema(
        responses={
            204: openapi.Response(description='Tag deleted successfully'),
            400: openapi.Response('Tag not found', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    )
    def destroy(self, request, pk):
        tag = Tag.objects.filter(id=pk)
        if not tag.exists():
            return Response({
                "message": "Tag not found"
            }, status=400)

        tag.delete()

        return Response(status=204)
    
    @swagger_auto_schema(
        responses={
            200: TagSerializer(many=True),
        }
    )
    def list(self, request):
        return Response(TagSerializer(
            Tag.objects.all(), many=True
        ).data, status=200)
