from django.test import TestCase, RequestFactory
from django.apps import apps
from django.template import Context, Template
from apps.MySearch.apps import MysearchConfig

# Create your tests here.


class MySearchTest(TestCase):
    fixtures = ['mysearch_testdata.json']

    def test_mysearch_get_status(self):
        '''
        This just tests the basic search form (get) to ensure it is valid
        '''
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_mysearch_get_content(self):
        '''
        This just tests the basic search form (get) to ensure it is valid
        '''
        response = self.client.get('/search/')
        self.assertContains(response, 'Search')

    def test_mysearch_aws(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.post("/search/", {'form_searchText': "AWS"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("AWS", str(response.content))

    def test_mysearch_python(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.post("/search/", {'form_searchText': "Python"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Python", str(response.content))
