from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from django.db import models
from pydc.context.models import *
from datetime import *
from decimal import Decimal

def debug(request):
    return HttpResponse(repr(request))

def getChannels(chanID=None, name=None, derived=None):
    "Return django object of all the data channels, optionally filtered"
    filter = {}
    if chanID is not None:
        filter["chanID"] = chanID
    if name is not None:
        filter["name"] = name
    if derived is not None:
        filter["derived"] = derived
    channels = DataChannel.objects.filter(**filter)
    return HttpResponse('[%s]' % (', '.join([c.asJSON(), for c in channels])))
