from django.shortcuts import render
from rest_framework import status,generics
from django_filters.rest_framework import DjangoFilterBackend,filters,FilterSet
from .models import *
from .serializers import CandidateSerializer
# Create your views here.


def index(request):
    return render(request, "voteapp/index.html")


class CandidateViewSet(generics.ListAPIView):
    serializer_class = CandidateSerializer
    queryset = Candidate.object.all()
    filter_backends = [DjangoFilterBackend]
    permission_classes = [

    ]

