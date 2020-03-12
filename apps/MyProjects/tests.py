from django.test import TestCase, RequestFactory
from django.apps import apps
from django.template import Context, Template
from apps.MyProjects.apps import MyprojectsConfig
from apps.MyProjects.models import ProjectLanguage, MyProject

# Create your tests here.


class MyProjectsTest(TestCase):
    fixtures = ['myprojects_testdata.json']

    def test_myprojects_language_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/projects/2/')
        self.assertEqual(response.status_code, 200)

    def test_myprojects_language_content(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/projects/2/')
        self.assertContains(response, 'Python')

    def test_myprojects_project_detail_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/projects/detail/1/')
        self.assertEqual(response.status_code, 200)

    def test_myprojects_project_detail_content(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/projects/detail/1/')
        self.assertContains(response, 'main project description')

    def test_myprojects_nl_project_detail_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/projects/nldetail/1/')
        self.assertEqual(response.status_code, 200)

    def test_myprojects_nl_project_detail_content(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/projects/nldetail/1/')
        self.assertContains(response, 'main project description')

        # Ensure the page does not contain the next or previous link.
        self.assertNotContains(response, '>next')
        self.assertNotContains(response, 'previous<')

    def test_apps(self):
        '''
        This test for apps was recommended here:
        https://stackoverflow.com/questions/43334953/testing-apps-py-in-django/45613899
        '''
        self.assertEqual(MyprojectsConfig.name, 'MyProjects')
        self.assertEqual(apps.get_app_config('MyProjects').name,
                         'apps.MyProjects')

    def test_projectlanguage_str(self):
        '''
        Test the string representation of project language
        '''
        tstLanguage = ProjectLanguage(title="TEST TITLE")
        self.assertEqual(str(tstLanguage), tstLanguage.title)

    def test_myproject_str(self):
        '''
        Test the string representation of myproject
        '''
        tstMyProject = MyProject(title="TEST TITLE")
        self.assertEqual(str(tstMyProject), tstMyProject.title)

    def test_projectlanguage_absolute_url(self):
        '''
        Test the absolute_url of the project returns something sensible.
        KEY - The test data has a pk of 2 (Python)
        '''
        objL = ProjectLanguage.objects.get(pk=2)
        strURL = objL.get_absolute_url()
        self.assertIn("projects/2", strURL)

    def test_myproject_absolute_url(self):
        '''
        Test the absolute_url of the project returns something sensible.
        KEY - The test data has a pk of 1 (Test Python Project)
        '''
        objL = MyProject.objects.get(pk=1)
        strURL = objL.get_absolute_url()
        self.assertIn("projects/detail/1", strURL)
