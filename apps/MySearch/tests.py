from django.test import TestCase, RequestFactory
from django.apps import apps
from django.template import Context, Template
from apps.MySearch.apps import MysearchConfig
from apps.MySearch.views import DualPage, DualPaginator
from apps.MyProjects.models import MyProject
from apps.Training.models import TrainingCourse
from django.db.models import Q

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
        response = self.client.get("/search/", {'form_searchText': "AWS"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("AWS", str(response.content))

    def test_mysearch_python(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get("/search/", {'form_searchText': "Python"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Python", str(response.content))

    def test_paginator(self):
        '''
        This tests the Dual Paginator used by the search view
        '''

        # Define a basic search text of the letter  'a'
        search_text = 'a'

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

        # Define a basic path for the test
        strPath = '/'

        # Set the paginator
        objPaginator = DualPaginator(training_results, project_results,
                                     strPath)

        # Test count, num_pages
        self.assertEqual(objPaginator.count(), 2)
        self.assertEqual(objPaginator.num_pages(), 1)

        # Get the first page
        objPage = objPaginator.page(1)

        # Ensure there is no next and previous page
        self.assertEqual(objPage.has_next(), False)
        self.assertEqual(objPage.has_previous(), False)

        # Get the previous and next page number
        self.assertEqual(objPage.previous_page_number(), 0)
        self.assertEqual(objPage.next_page_number(), 2)

        # Get the previous and next page link
        self.assertEqual(objPage.previous_page_link(), '/&pageNo=0')
        self.assertEqual(objPage.next_page_link(), '/&pageNo=2')
