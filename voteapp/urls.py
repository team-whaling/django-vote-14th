from django.urls import path
from . import views
from .views import *

app_name = 'voteapp'   # 어플리케이션의 이름공간 설정.
## 제너릭 뷰 사용하기.

urlpatterns = [
    path(r'candidate', CandidateViewSet.as_view())
]