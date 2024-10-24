from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest


def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    return HttpResponse("Hello")