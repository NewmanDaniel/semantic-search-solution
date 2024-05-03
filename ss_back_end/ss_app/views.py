from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ss_app.semantic_search import get_top_k_similar_proposals
from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def view_get_top_k_similar_proposals(request):
    # TODO refactor this into a serializer
    proposal_description = str(request.data.get('text_to_search'))
    top_k = int(request.data.get('k'))
    task = get_top_k_similar_proposals.delay(proposal_description, top_k=top_k)
    return Response({"task_id": task.id})

@csrf_exempt
@api_view(['GET'])
def get_task_result(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return Response({"status": "completed", "result": task_result.result})
    return Response({"status": "pending"})
