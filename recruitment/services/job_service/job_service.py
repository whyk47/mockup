from django.http import HttpRequest
from django.db.models.query import QuerySet
from django.db.models import Q

from ...models import Job
from ..location_service.location_service import LocationService
from ..location_service.location_service_exceptions import NoAddressException

from datetime import datetime, timedelta


class JobService:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(JobService, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        self.loc = LocationService()

    def filter(self, request: HttpRequest) -> dict[str, QuerySet[Job] | str]:
        loc = self.loc
        queryset = Job.objects
        req = request.GET.dict()
        if req.get('query'):
            queryset = queryset.filter(
                Q(title__icontains=req.get('query')) |
                Q(description__icontains=req.get('query')) |
                Q(company__icontains=req.get('query')) |
                Q(address__icontains=req.get('query')) |
                Q(job_type__icontains=req.get('query'))
            )
        if req.get('min_salary'):
            queryset = queryset.filter(monthly_pay__gte=req.get('min_salary'))
        if req.get('max_salary'):
            queryset = queryset.filter(monthly_pay__lte=req.get('max_salary'))
        if req.get('address') and req.get('radius'):
            queryset = loc.dist_filter(queryset, req.get('address'), int(req.get('radius')) or 20)

        if req.get('remote') == 'remote_only':
            queryset = queryset.filter(remote=True)
        if req.get('full_time') == None:
            queryset = queryset.exclude(job_type=Job.JobType.FULL_TIME)
        if req.get('part_time') == None:
            queryset = queryset.exclude(job_type=Job.JobType.PART_TIME)
        if req.get('intern') == None:
            queryset = queryset.exclude(job_type=Job.JobType.INTERN)

        match req.get('date'):
            case 'week':
                queryset = queryset.filter(created_at__gte=datetime.now() - timedelta(days=7))
            case 'month':
                queryset = queryset.filter(created_at__gte=datetime.now() - timedelta(days=30))
            case 'year':
                queryset = queryset.filter(created_at__gte=datetime.now() - timedelta(days=365))
        
        try:
            match req.get('sort'): 
                case 'salary_low':
                    queryset = queryset.order_by('monthly_pay')
                case 'salary_high':
                    queryset = queryset.order_by('-monthly_pay')
                case 'dist_low':
                    queryset = loc.dist_sort(queryset, req.get('address'))
                case 'newest':
                    queryset = queryset.order_by('-created_at')
        except NoAddressException as e:
            error = str(e)
            return {'jobs': queryset.all(), 'error': error}
        return {'jobs': queryset.all()}
    

    def job(self, job_id: int) -> Job:
        return Job.objects.get(id=job_id)