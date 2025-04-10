from django.shortcuts import render
from .task import analyze_repo_task
from django.http import JsonResponse
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# Create your views here.
def start_task(request):
    if request.method == "POST":
        try:
            url=request.POST.get('url')
            pr_number=request.POST.get('pr_number')
            github_token = request.POST.get('github_token')

            task = analyze_repo_task.delay(url, pr_number, github_token)
            return JsonResponse({"task_id": task.id, "status": "Task started"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)   


def task_status_view(request, task_id):
    result = AsyncResult(task_id)

    response = {
        'task_id': task_id,
        'status': result.state,
    }

    if result.state == 'SUCCESS':
        response['result'] = result.result
    elif result.state == 'FAILURE':
        response['error'] = str(result.result)

    return JsonResponse(response)