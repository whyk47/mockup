from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from .models import *


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    return render(request, 'recruitment/index.html', {
        'jobs': Job.objects.all(),
    })

def details(request: HttpRequest, job_id: int) -> HttpResponse | HttpResponseRedirect:
    return HttpResponse(f'Job {job_id}')