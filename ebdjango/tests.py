from django.test import SimpleTestCase, TestCase, RequestFactory
from ebdjango.scripts.AWSParameterStore import AWSParameterStore
from ebdjango.scripts.GeneralFunctions import appendEC2IPToArray

# Create your tests here.


class EBDjangoTestSimple(SimpleTestCase):

    def test_parameter_store(self):
        '''
        This creates an AWSParameterStore object and then uses it to extract a
        parameter.   I have a test parameter setup specifically for the test.
        '''

        # Define variables for the test parameter that I am going to access
        AWS_PSTORE_PROJECT = '/MarksWebsite/'
        AWS_PSTORE_ENV = 'test'
        AWS_PSTORE_REGION = 'eu-west-2'

        # Setup the parameter store object and get the PARAMSTORE_TEST from
        # the store
        objStore = AWSParameterStore(AWS_PSTORE_PROJECT,
                                     AWS_PSTORE_ENV,
                                     AWS_PSTORE_REGION)
        res = objStore.get_parameter("PARAMSTORE_TEST", False)

        # Test
        self.assertEqual(res, "SUCCESS")

    def test_add_ec2ip(self):
        '''
        I cannot do a huge amount with this because the ip can be different
        depending on the EC2 instance and if you are running it locally etc.
        '''

        # Create an empty list
        lstIn = []

        # Try to run the function against it
        ret = appendEC2IPToArray(lstIn)

        # Assert result must be True or False
        self.assertIn(ret, [True, False])


class EBDjangoTest(TestCase):

    def test_sitemap_status(self):
        '''
        The home page is also the page displayed by the AboutMe app
        '''
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
