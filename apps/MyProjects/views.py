from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.utils.safestring import mark_safe
from apps.MyProjects.models import ProjectLanguage, MyProject

import logging
logger = logging.getLogger('ebdjango')

# Create your views here.


class ProjectLanguageView(View):
    def get(self, request, **kwargs):
        logger.debug('Logging debug message')
        intPK = self.kwargs['pk']
        language = ProjectLanguage.objects.get(pk=intPK)
        projects = language.myproject_set.all()
        context = {
            'language': language,
            'projects': projects,
        }
        return render(request, 'language.html', context=context)


class ProjectDetailView(View):

    def __init__(self):
        self._contextData = None
        self._intPK = None
        self._project = None
        self._intLangID = None

    def _buildContextData(self, request,  **kwargs):
        '''
        This is used to build the context data that we are going to send
        to the template. I have done it this way because I want to build
        two versions of the class.   One that has a previous/next project
        link, but another class that does not.   This base class does not
        have the previous/next link.
        '''

        # Get the primary key of the Project and the corresponding
        # MyProject object
        self._intPK = self.kwargs['pk']
        self._project = MyProject.objects.get(pk=self._intPK)

        # get the formatted date
        formatedDate = self._project.date.strftime("%d-%b-%Y")

        # Either throw a 404 or get the group id of the training course
        if not self._project.language:
            raise Http404

        # Store the language id
        self._intLangID = self._project.language.id

        # Build the contextData
        self._contextData = {
            'project': self._project,
            'projectHTML': mark_safe(self._project.main_text),
            'formatedDate': formatedDate,
            'language': self._project.language,
            'prev': None,
            'next': None,
        }

    def get(self, request, **kwargs):

        logger.debug('Logging debug message')

        # Build the context data
        self._buildContextData(request, **kwargs)

        # Now send the data to the template
        return render(request, 'project_detail.html',
                      context=self._contextData)


class ProjectDetailViewWithLinks(ProjectDetailView):

    def __init__(self):
        super().__init__()

    def _buildContextData(self, request,  **kwargs):
        super()._buildContextData(request, **kwargs)

    def _buildPrevAndNext(self, request):
        '''
        This should be run after _buildContextData and adds the extra
        data into the context for displaying the previous and next links.
        '''

        # Filter TrainingCourse table to a list containing the same group
        # id of this course
        filtProjects = MyProject.objects.filter(language_id=self._intLangID)

        # GEt the position of the primary key in the list
        projectIndex = (*filtProjects,).index(self._project)

        # Get the next course
        if len(filtProjects)-1 > projectIndex:
            nextProject = filtProjects[projectIndex+1]
            self._contextData['next'] = nextProject

        # Get the previous course
        if projectIndex > 0:
            prevCourse = filtProjects[projectIndex-1]
            self._contextData['prev'] = prevCourse

    def get(self, request, **kwargs):

        logger.debug('Logging debug message')

        # First, build the context data in a similar manner to the
        # ProjectDetailView class
        self._buildContextData(request, **kwargs)

        # Next, add the next and prev data onto the context data
        self._buildPrevAndNext(request)

        # Finally render the template
        return render(request, 'project_detail.html',
                      context=self._contextData)
