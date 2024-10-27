from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from .models import *


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    queryset = Job.objects.all()
    if request.GET.get('query'):
        queryset = queryset.filter(title__icontains=request.GET.get('query'))
    if request.GET.get('min_salary'):
        queryset = queryset.filter(monthly_pay__gte=request.GET.get('min_salary'))
    if request.GET.get('max_salary'):
        queryset = queryset.filter(monthly_pay__lte=request.GET.get('max_salary'))
    return render(request, 'recruitment/index.html', {
        'jobs': queryset,
        **request.GET.dict(),
    })

def details(request: HttpRequest, job_id: int) -> HttpResponse | HttpResponseRedirect:
    return HttpResponse(f'Job {job_id}')