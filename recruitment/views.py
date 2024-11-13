from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.db.models import Q

from datetime import datetime, timedelta

from .models import *
from .services.location_service.location_service import LocationService
from .services.location_service.location_service_exceptions import NoAddressException

loc = LocationService()


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    error = None
    queryset = Job.objects
    if request.GET.get('query'):
        queryset = queryset.filter(
            Q(title__icontains=request.GET.get('query')) |
            Q(description__icontains=request.GET.get('query')) |
            Q(company__icontains=request.GET.get('query')) |
            Q(address__icontains=request.GET.get('query')) |
            Q(job_type__icontains=request.GET.get('query'))
        )
    if request.GET.get('min_salary'):
        queryset = queryset.filter(monthly_pay__gte=request.GET.get('min_salary'))
    if request.GET.get('max_salary'):
        queryset = queryset.filter(monthly_pay__lte=request.GET.get('max_salary'))
    if request.GET.get('address') and request.GET.get('radius'):
        queryset = loc.dist_filter(queryset, request.GET.get('address'), int(request.GET.get('radius')) or 20)

    if request.GET.get('remote') == 'remote_only':
        queryset = queryset.filter(remote=True)
    if request.GET.get('full_time') == None:
        queryset = queryset.exclude(job_type=Job.JobType.FULL_TIME)
    if request.GET.get('part_time') == None:
        queryset = queryset.exclude(job_type=Job.JobType.PART_TIME)
    if request.GET.get('intern') == None:
        queryset = queryset.exclude(job_type=Job.JobType.INTERN)

    match request.GET.get('date'):
        case 'week':
            queryset = queryset.filter(created_at__gte=datetime.now() - timedelta(days=7))
        case 'month':
            queryset = queryset.filter(created_at__gte=datetime.now() - timedelta(days=30))
        case 'year':
            queryset = queryset.filter(created_at__gte=datetime.now() - timedelta(days=365))
    
    try:
        match request.GET.get('sort'): 
            case 'salary_low':
                queryset = queryset.order_by('monthly_pay')
            case 'salary_high':
                queryset = queryset.order_by('-monthly_pay')
            case 'dist_low':
                queryset = loc.dist_sort(queryset, request.GET.get('address'))
            case 'newest':
                queryset = queryset.order_by('-created_at')
    except NoAddressException as e:
        error = str(e)
    return render(request, 'recruitment/index.html', {
        'jobs': queryset.all(),
        **request.GET.dict(),
        'error': error
    })

def details(request: HttpRequest, job_id: int) -> HttpResponse | HttpResponseRedirect:
    return HttpResponse(f'Job {job_id}')