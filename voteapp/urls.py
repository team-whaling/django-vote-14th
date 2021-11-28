from django.urls import path, include
from rest_framework import routers
from . import views
from .views import *

app_name = 'voteapp'   # 어플리케이션의 이름공간 설정.

router = routers.DefaultRouter()
router.register(r'candidates', views.CandidateViewSet)

urlpatterns = [
    path('', include(router.urls))
]