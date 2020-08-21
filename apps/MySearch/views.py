from django.shortcuts import render
from django.views import View
from apps.MySearch.forms import SearchForm
from apps.MyProjects.models import MyProject
from apps.Training.models import TrainingCourse
from django.db.models import Q
from django.core.paginator import Paginator
import math


import logging
logger = logging.getLogger('ebdjango')

# Create your views here.


class DualPage():

    def __init__(self, number, trainingPage, projectsPage, strPath):
        self.number = number
        self.trainingPage = trainingPage
        self.projectsPage = projectsPage
        self.__strBasePath = strPath

    def has_next(self):

        boolNext = False

        if self.trainingPage is not None:
            boolNext = boolNext or self.trainingPage.has_next()
        if self.projectsPage is not None:
            boolNext = boolNext or self.projectsPage.has_next()

        return boolNext

    def has_previous(self):
        boolPrev = False

        if self.trainingPage is not None:
            boolPrev = boolPrev or self.trainingPage.has_previous()
        if self.projectsPage is not None:
            boolPrev = boolPrev or self.projectsPage.has_previous()

        return boolPrev

    def previous_page_number(self):
        return self.number-1

    def next_page_number(self):
        return self.number+1

    def previous_page_link(self):
        strRet = self.__strBasePath + '&pageNo=' \
                + str(self.previous_page_number())
        return strRet

    def next_page_link(self):
        strRet = self.__strBasePath + '&pageNo=' + str(self.next_page_number())
        return strRet


class DualPaginator():

    def __init__(self, training_results, project_results, strPath):

        self.C_NO_PER_PAGE = 6
        self.__trainingPaginator = Paginator(training_results,
                                             self.C_NO_PER_PAGE)
        self.__projectPaginator = Paginator(project_results,
                                            self.C_NO_PER_PAGE)
        self.__strBasePath = strPath

    def count(self):
        # Total number of records
        total = self.__trainingPaginator.count + self.__projectPaginator.count
        return total

    def num_pages(self):
        # Must cover both query-sets, so return the max of both
        maxPages = max(self.__trainingPaginator.num_pages,
                       self.__projectPaginator.num_pages)
        return maxPages

    def page(self, intPageNo):
        objTraining = None
        if intPageNo <= self.__trainingPaginator.num_pages:
            objTraining = self.__trainingPaginator.page(intPageNo)
        objProjects = None
        if intPageNo <= self.__projectPaginator.num_pages:
            objProjects = self.__projectPaginator.page(intPageNo)
        objPage = DualPage(intPageNo, objTraining, objProjects,
                           self.__strBasePath)
        return objPage


class SearchView(View):

    def get(self, request, **kwargs):
        # Assume link from search button etc as there is no GET data, so just
        # initiate the form
        logger.debug('Logging debug message')

        form = SearchForm(request.GET)

        page = DualPage(1, None, None, "/")

        context = {
            'form': form,
            'page': page,
            'noPages': 1,
        }

        if form.is_valid():

            # Get the Search Text
            search_text = form.cleaned_data['form_searchText'].strip()

            # Get the training and project results.
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

            # Try to get the page number from the link
            intPageNo = 1
            if 'pageNo' in request.GET:
                intPageNo = int(request.GET['pageNo'])

            # Get the path.   Assume it ends in ...&pageno=..., so just
            # get the first part.   Used to generate links later.
            strPath = request.get_full_path()
            strPath = strPath.split("&")[0]

            # Set the paginator
            objPaginator = DualPaginator(training_results, project_results,
                                         strPath)

            # If the page is out of range, set it to min/max
            intPageNo = max(intPageNo, 1)
            intPageNo = min(intPageNo, objPaginator.num_pages())

            # Get the page
            page = objPaginator.page(intPageNo)

            # Update the context
            context["page"] = page
            context['noPages'] = objPaginator.num_pages

        return render(request, 'search.html', context=context)
