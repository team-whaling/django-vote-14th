from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'voteapp'   # 어플리케이션의 이름공간 설정.

router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet)

urlpatterns = [
    path('register/', Registartion.as_view()),
    path('login/', Login.as_view()),
    path('', include(router.urls))
]