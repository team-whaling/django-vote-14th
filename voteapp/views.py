from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import status, generics, viewsets
# Need For using JWT
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class Registartion(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Register Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        },
            status=status.HTTP_201_CREATED)


class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Login Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['username'] == "None":
            return Response({"message": "Login Fail"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": user['token']
            }
        )


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        user = request.user
        # 유저가 로그인하지 않은 경우
        if not user.is_authenticated:
            return Response("X", status=status.HTTP_403_FORBIDDEN)
        # 유저가 로그인한 경우
        else:
            # 이미 투표한 유저의 경우
            if user.voted:
                return Response("Already voted", status=status.HTTP_403_FORBIDDEN)
            # 유저 투표 여부 체크 및 후보자 득표 수 증가
            user.voted = True
            user.save()
            candidate = self.get_object()
            candidate.vote += 1
            candidate.save()
            return Response("O")
