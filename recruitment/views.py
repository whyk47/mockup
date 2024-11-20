from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.admin.views.decorators import staff_member_required

from .services.job_service.job_service import JobService
from .util import *

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
    # TODO: Pagination
    # page = get_page(request, job.filter(request).pop('jobs'))
    return render(request, 'recruitment/search.html', {
        # 'page': page,
        **job.filter(request),
        **request.GET.dict(),
    })

@staff_member_required
def generate(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    job.generate_jobs(scrape=False, process=False)
    return HttpResponse('Jobs generated')