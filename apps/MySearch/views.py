from django.shortcuts import render
from django.views import View
from apps.MySearch.forms import SearchForm
from apps.MyProjects.models import MyProject
from apps.Training.models import TrainingCourse
from django.db.models import Q
import math


import logging
logger = logging.getLogger('ebdjango')

# Create your views here.


class SearchView(View):

    def get(self, request, **kwargs):
        # Assume link from search button etc as there is no GET data, so just
        # initiate the form
        logger.debug('Logging debug message')
        form = SearchForm()
        context = {
            'form': form,
            'training_results': None,
            'project_results': None,
        }
        return render(request, 'search.html', context=context)

    def post(self, request, **kwargs):

        logger.debug('Logging debug message')

        # Assume some data has been sent so try to validate the form
        form = SearchForm(request.POST)

        context = {
            'form': form,
            'training_results': None,
            'project_results': None,
        }

        if form.is_valid():

            # Get the Search Text
            search_text = form.cleaned_data['form_searchText'].strip()

            training_results = TrainingCourse.objects.filter(
                                    Q(title__icontains=search_text) |
                                    Q(short_text__icontains=search_text) |
                                    Q(main_text__icontains=search_text)
                                )
            project_results = MyProject.objects.filter(
                                    Q(title__icontains=search_text) |
                                    Q(short_text__icontains=search_text) |
                                    Q(main_text__icontains=search_text)
                                )

            context["training_results"] = training_results
            context["project_results"] = project_results

        # Initiate the form with previous form data
        return render(request, 'search.html', context=context)
