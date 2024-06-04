from django.shortcuts import render

# Create your views here.

def homepage(request, *args, **kwargs):
    from django.http import HttpResponse
    return HttpResponse("homepage no implementado", content_type="text/plain")
