from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend,filters,FilterSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# Need For using JWT
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
@permission_classes([AllowAny]) # 인증 필요없다
class Registartion(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message" : "Register Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        return Response({
            "user" : UserSerializer(user, context=self.get_serializer_context()).data
        },
        status = status.HTTP_201_CREATED)



@permission_classes([AllowAny]) # 인증 필요없다
class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message" : "Login Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['username'] == "None":
            return Response({"message" : "Login Fail"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "user" : UserSerializer(user, context=self.get_serializer_context()).data,
                "token" : user['token']
            }
        )


class CandidateViewSet(generics.ListAPIView):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()