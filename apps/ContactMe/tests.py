from django.test import TestCase, RequestFactory
from django.apps import apps
from django.template import Context, Template
from apps.ContactMe.apps import ContactmeConfig
from apps.ContactMe.forms import ContactForm

# Create your tests here.


class ContactMeTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_contactme_page_status(self):
        '''
        Check the contactme page returns status 200
        '''
        response = self.client.get('/contactme/')
        self.assertEqual(response.status_code, 200)

    def test_contactme_page_content(self):
        '''
        Check the contactme page contains the text Contact Me
        '''
        response = self.client.get('/contactme/')
        self.assertContains(response, 'Contact Me')

    def test_apps(self):
        '''
        This test for apps was recommended here:
        https://stackoverflow.com/questions/43334953/testing-apps-py-in-django/45613899
        '''
        self.assertEqual(ContactmeConfig.name, 'ContactMe')
        self.assertEqual(apps.get_app_config('ContactMe').name,
                         'apps.ContactMe')

    def test_contactform_valid(self):
        '''
        I have used this:
        https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
        '''
        form = ContactForm(data={'form_name': "Mark Wilson",
                                 'form_email': "mark_john_wilson@yahoo.co.uk",
                                 'form_subject': "UNIT TEST - CONTACTME",
                                 'form_message': "TEST CONTACTFORM IN "
                                                 "CONTACTME APP"})
        self.assertTrue(form.is_valid())

    def test_contactform_invalid(self):
        '''
        I have used this:
        https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
        '''
        form = ContactForm(data={'form_name': "",
                                 'form_email': "",
                                 'form_subject': "",
                                 'form_message': ""})
        self.assertFalse(form.is_valid())

    def test_contactform_post(self):
        '''
        With this test, I post a valid version of the form, so it should
        actually send an email and I should get a valid response.
        '''
        postData = {'form_name': "Mark Wilson",
                    'form_email': "mark_john_wilson@yahoo.co.uk",
                    'form_subject': "UNIT TEST - CONTACTME",
                    'form_message': "TEST CONTACTFORM IN CONTACTME APP"
                    }
        response = self.client.post("/contactme/", postData)
        self.assertEqual(response.status_code, 200)
        self.assertIn("I appreciate you contacting me", str(response.content))

    def test_contactform__invalid_post(self):
        '''
        With this test, I post a valid version of the form, so it should
        actually send an email and I should get a valid response.
        '''
        postData = {'form_name': "Mark Wilson",
                    'form_email': "",
                    'form_subject': "UNIT TEST - CONTACTME",
                    'form_message': "TEST CONTACTFORM IN CONTACTME APP"}
        response = self.client.post("/contactme/", postData)

        # The form should post successfully.
        self.assertEqual(response.status_code, 200)

        # It should also contain the valid text that was previously posted
        strC = str(response.content)
        self.assertIn("Mark Wilson", strC)
        self.assertIn("UNIT TEST - CONTACTME", strC)
        self.assertIn("TEST CONTACTFORM IN CONTACTME APP", strC)
