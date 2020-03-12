from django.test import TestCase, RequestFactory
from django.apps import apps
from django.template import Context, Template
from apps.AboutMe.apps import AboutmeConfig

# Create your tests here.


class AboutMeTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_home_page_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_content(self):
        '''
        The home page should have an ABOUT ME and RESUME present
        '''
        response = self.client.get('/')
        self.assertContains(response, 'About Me')
        self.assertContains(response, 'Resume')

    def test_apps(self):
        '''
        This test for apps was recommended here:
        https://stackoverflow.com/questions/43334953/testing-apps-py-in-django/45613899
        '''
        self.assertEqual(AboutmeConfig.name, 'AboutMe')
        self.assertEqual(apps.get_app_config('AboutMe').name, 'apps.AboutMe')

    def test_templatetags_addstr(self):
        '''
        This tests templatetags to ensure the addstr function works.   I used
        the following:
        https://krzysztofzuraw.com/blog/2017/how-to-test-django-template-tags.html
        '''
        context = Context({'inFile': 'myfile.jpg'})

        strTemplate = '<html>{% load global_functions %}<body>'\
                      '<img src="{{ \'/img/\'|addstr:inFile }}"></body></html>'
        template_to_render = Template(strTemplate)
        rendered_template = template_to_render.render(context)

        self.assertIn('"/img/myfile.jpg"', rendered_template)

    def test_templatetags_linkValid(self):
        '''
        This tests templatetags to ensure the linkValid function works.   I
        used the following:
        https://krzysztofzuraw.com/blog/2017/how-to-test-django-template-tags.html
        '''

        strTemplate = '<html>{% load global_functions %}<body>{% if course.'\
                      'code_text|linkValid:course.link_href %}OK{% endif %}'\
                      '</body></html>'

        # When context contains two None's then OK should not appear
        context = Context({'course': {'code_text': None, 'link_href': None}})
        template_to_render = Template(strTemplate)
        rendered_template = template_to_render.render(context)
        self.assertNotIn('OK', rendered_template)

        # When one context is None's then OK should not appear
        context = Context({'course': {'code_text': 'aaa', 'link_href': None}})
        template_to_render = Template(strTemplate)
        rendered_template = template_to_render.render(context)
        self.assertNotIn('OK', rendered_template)

        # When one context is None's then OK should not appear
        context = Context({'course': {'code_text': None, 'link_href': 'bbb'}})
        template_to_render = Template(strTemplate)
        rendered_template = template_to_render.render(context)
        self.assertNotIn('OK', rendered_template)

        # When both are present OK should appear
        context = Context({'course': {'code_text': 'aaa', 'link_href': 'bbb'}})
        template_to_render = Template(strTemplate)
        rendered_template = template_to_render.render(context)
        self.assertIn('OK', rendered_template)

        # If either has length less than 1, then OK should not appear
        context = Context({'course': {'code_text': '', 'link_href': 'bbb'}})
        template_to_render = Template(strTemplate)
        rendered_template = template_to_render.render(context)
        self.assertNotIn('OK', rendered_template)
