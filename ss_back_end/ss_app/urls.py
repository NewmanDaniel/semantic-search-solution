# In ss_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get-top-k-similar-proposals/', views.view_get_top_k_similar_proposals, name='call_get_top_k_similar_proposals'),
    path('task-result/<str:task_id>/', views.get_task_result, name='get_task_result'),
]
