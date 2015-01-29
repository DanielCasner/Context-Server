from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

def default(request):
    return HttpResponse(repr(request))
