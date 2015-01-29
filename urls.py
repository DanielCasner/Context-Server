from django.conf.urls.defaults import *

urlpatterns = patterns('',
                           ('^$', 'pydc.context.views.default'),
                       )
