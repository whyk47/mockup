from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.db.models import Q

from .models import *
from .services.location_service.location_service import LocationService

loc = LocationService()


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    queryset = Job.objects
    if request.GET.get('query'):
        queryset = queryset.filter(
            Q(title__icontains=request.GET.get('query')) |
            Q(description__icontains=request.GET.get('query')) |
            Q(company__icontains=request.GET.get('query')) |
            Q(address__icontains=request.GET.get('query'))
        )
    if request.GET.get('min_salary'):
        queryset = queryset.filter(monthly_pay__gte=request.GET.get('min_salary'))
    if request.GET.get('max_salary'):
        queryset = queryset.filter(monthly_pay__lte=request.GET.get('max_salary'))
    if request.GET.get('address'):
        queryset = loc.dist_filter(queryset, request.GET.get('address'), int(request.GET.get('radius')) or 20)
    # if request.GET.get('sort'):
    #     match request.GET.get('sort'): 
    
    return render(request, 'recruitment/index.html', {
        'jobs': queryset.all(),
        **request.GET.dict(),
    })

def details(request: HttpRequest, job_id: int) -> HttpResponse | HttpResponseRedirect:
    return HttpResponse(f'Job {job_id}')