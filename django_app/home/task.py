from celery import Celery
from celery import shared_task
from home.utils.agent import analyze_all_files

app=Celery("django_app")
app.config_from_object('django.conf:settings',namespace="CELERY")

@shared_task
def analyze_repo_task(url, repo, github_token=None):
    print(f"Starting task for URL: {url}, PR: {repo}")
    result = analyze_all_files(url, repo, github_token=None)
    print(f"Task completed with result: {result}")
    return result
