from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from .services.job_service.job_service import JobService

job = JobService()


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    return render(request, 'recruitment/index.html', {
        **job.filter(request),
        **request.GET.dict(),
    })

def details(request: HttpRequest, job_id: int) -> HttpResponse | HttpResponseRedirect:
    return render(request, 'recruitment/job.html', {
        'job': job.job(job_id),
    })

def search(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    return render(request, 'recruitment/search.html', {
        **job.filter(request),
        **request.GET.dict(),
    })