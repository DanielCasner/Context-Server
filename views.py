from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from django.db import models
from pydc.context.models import *
from datetime import *
from decimal import Decimal

def debug(request):
    return HttpResponse(repr(request))

def getChannels(id=None, name=None, derived=None):
    "Return django object of all the data channels, optionally filtered"
