from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.utils.safestring import mark_safe
from apps.Training.models import TrainingGroup
from apps.Training.models import TrainingCourse

import logging
logger = logging.getLogger('ebdjango')

# Create your views here.


class TrainingView(View):
    def get(self, request, **kwargs):
        logger.debug('Logging debug message')
        intPK = self.kwargs['pk']
        group = TrainingGroup.objects.get(pk=intPK)
        courses = group.trainingcourse_set.all()
        context = {
            'group': group,
            'courses': courses,
        }
        return render(request, 'training.html', context=context)


class TrainingDetailView(View):

    def __init__(self):
        self._contextData = None
        self._intPK = None
        self._course = None
        self._intGp = None

    def _buildContextData(self, request,  **kwargs):
        '''
        This is used to build the context data that we are going to send to
        the template. I have done it this way because I want to build two
        versions of the class.   One that has a previous/next project link,
        but another class that does not.   This base class does not have the
        previous/next link.
        '''

        # Get the primary key of the Training Course and the corresponding
        # TrainingCourse object
        self._intPK = self.kwargs['pk']
        self._course = TrainingCourse.objects.get(pk=self._intPK)

        # Either throw a 404 or get the group id of the training course
        if not self._course.group:
            raise Http404
        self._intGp = self._course.group.id

        # get the formatted date
        formatedDate = self._course.date.strftime("%d-%b-%Y")

        # Build the context to send to the template.
        self._contextData = {
            'course': self._course,
            'courseHTML': mark_safe(self._course.main_text),
            'formatedDate': formatedDate,
            'group': self._course.group,
            'prev': None,
            'next': None,
        }

    def get(self, request, **kwargs):

        logger.debug('Logging debug message')

        # Build the context data
        self._buildContextData(request, **kwargs)

        # Now send the data to the template
        return render(request, 'training_detail.html',
                      context=self._contextData)


class TrainingDetailViewWithLinks(TrainingDetailView):

    def __init__(self):
        super().__init__()

    def _buildContextData(self, request, **kwargs):
        super()._buildContextData(request, **kwargs)

    def _buildPrevAndNext(self, request):
        '''
        This should be run after _buildContextData and adds the extra data
        into the context for displaying the previous and next links.
        '''

        # Filter TrainingCourse table to a list containing the same group
        # id of this course
        filtGroup = TrainingCourse.objects.filter(group_id=self._intGp)

        # Get the position of the primary key in the list
        courseIndex = (*filtGroup,).index(self._course)

        # Get the next course
        if len(filtGroup)-1 > courseIndex:
            nextCourse = filtGroup[courseIndex+1]
            self._contextData['next'] = nextCourse

        # Get the previous course
        if courseIndex > 0:
            prevCourse = filtGroup[courseIndex-1]
            self._contextData['prev'] = prevCourse

    def get(self, request, **kwargs):

        logger.debug('Logging debug message')

        # First, build the context data in a similar manner to the
        # TrainingDetailView class
        self._buildContextData(request, **kwargs)

        # Next, add the next and prev data onto the context data
        self._buildPrevAndNext(request)

        return render(request, 'training_detail.html',
                      context=self._contextData)
