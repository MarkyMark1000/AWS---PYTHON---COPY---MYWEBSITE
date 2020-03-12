from django.test import TestCase, RequestFactory
from django.apps import apps
from django.template import Context, Template
from apps.Training.apps import TrainingConfig
from apps.Training.models import TrainingGroup, TrainingCourse

# Create your tests here.


class TrainingTest(TestCase):
    fixtures = ['training_testdata.json']

    def test_myprojects_language_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/training/1/')
        self.assertEqual(response.status_code, 200)

    def test_myprojects_language_content(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/training/1/')
        self.assertContains(response, 'AWS')

    def test_myprojects_project_detail_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/training/detail/1/')
        self.assertEqual(response.status_code, 200)

    def test_myprojects_project_detail_content(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/training/detail/1/')
        self.assertContains(response, 'AWS CloudFormation')

    def test_myprojects_nl_project_detail_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/training/nldetail/1/')
        self.assertEqual(response.status_code, 200)

    def test_myprojects_nl_project_detail_content(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/training/nldetail/1/')
        self.assertContains(response, 'AWS CloudFormation')

        # Ensure the page does not contain the next or previous link.
        self.assertNotContains(response, '>next')
        self.assertNotContains(response, 'previous<')

    def test_apps(self):
        '''
        This test for apps was recommended here:
        https://stackoverflow.com/questions/43334953/testing-apps-py-in-django/45613899
        '''
        self.assertEqual(TrainingConfig.name, 'Training')
        self.assertEqual(apps.get_app_config('Training').name, 'apps.Training')

    def test_traininggroup_str(self):
        '''
        Test the string representation of training group
        '''
        tstGroup = TrainingGroup(title="TEST TITLE")
        self.assertEqual(str(tstGroup), tstGroup.title)

    def test_trainingcourse_str(self):
        '''
        Test the string representation of trainingcourse
        '''
        tstCourse = TrainingCourse(title="TEST TITLE")
        self.assertEqual(str(tstCourse), tstCourse.title)
