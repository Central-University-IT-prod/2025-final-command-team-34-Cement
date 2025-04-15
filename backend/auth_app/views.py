from uuid import uuid4

from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .models import User, MentorProfile
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer, ChangePasswordSerializer, ImageUploadSerializer
from .authentication import JWTAuthectication

from drf_yasg.utils import swagger_auto_schema


class AuthViewSet(ViewSet):
    permission_classes = [AllowAny, ]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={201: RegistrationSerializer()}
    )
    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Response('Login successful', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))}
    )
    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        token, role = serializer.authentication()

        return Response({
            "token": token,
            "role": role
        }, status=200)


class UsersAPIView(APIView):
    @swagger_auto_schema(
        responses={200: UserSerializer()}
    )
    def get(self, request):
        user = UserSerializer(instance=request.user)
        return Response(user.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer()}
    )
    def patch(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


class RetrieveUserAPIView(APIView):
    @swagger_auto_schema(
        responses={200: UserSerializer(), 404: 'User not found'}
    )
    def get(self, request, login):
        user = User.objects.filter(login=login)
        if not user.exists():
            return Response({
                "message": "user not found"
            }, status=404)
        user = UserSerializer(instance=user.first())
        return Response(user.data)


class UpdatePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={200: UserSerializer()}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserSerializer(instance=request.user).data)


class SetRatingView(APIView):
    def post(self, request, login):
        mentor = MentorProfile.objects.filter(mentor__login=login)
        if not mentor.exists():
            return Response({
                "message": "mentor not found"
            }, status=404)
        mentor = mentor.first()
        score = request.data.get("score")
        if not score:
            return Response({
                "message": "score must be specified"
            }, status=400)
        mentor.mentor_rating = score
        mentor.save()
        return Response({
            "message": "ok"
        })


class RatingView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "score": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Оценка ментора от 1 до 5",
                    minimum=1,
                    maximum=5
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="ok"
            ),
            404: openapi.Response(
                description="mentor not found"
            ),
        }
    )
    def post(self, request, login):
        mentor = MentorProfile.objects.filter(mentor__login=login)
        if not mentor.exists():
            return Response({
                "message": "mentor not found"
            }, status=404)
        mentor.first().update_rating(request.data.get("score"))

        return Response({
            "message": "ok"
        })


class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user: User = request.user
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data['image']
        user.profile_image = image
        user.save()

        return Response({
            "message": f"Image added"
        })
