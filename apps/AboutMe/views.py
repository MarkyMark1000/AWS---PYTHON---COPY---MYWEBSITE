from django.shortcuts import render
from django.views.generic import TemplateView

import logging
logger = logging.getLogger('ebdjango')

# Create your views here.


class AboutMeView(TemplateView):
    def get(self, request, **kwargs):
        logger.debug('Logging debug message')
        return render(request, 'index.html', context=None)
