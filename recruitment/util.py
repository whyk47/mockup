from django.core.paginator import Paginator, Page
from django.http import HttpRequest

from typing import Iterable


def get_page(request: HttpRequest, objects: Iterable) -> Page:
    paginator = Paginator(objects, 10)
    page_no = request.GET.get("page")
    page = paginator.get_page(page_no)
    return page