from django.shortcuts import render
from django.views import View
from apps.ContactMe.forms import ContactForm
import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import SuspiciousOperation, ValidationError
from ebdjango import settings
import requests

import logging
logger = logging.getLogger('ebdjango')


# Create your views here.

class ContactView(View):

    def __getRecaptchaSiteKey(self):
        # If we are in testing mode, use the google test sitekey:
        # https://developers.google.com/recaptcha/docs/faq
        # G_TESTING is normally False, but set to True in tests.py
        if settings.G_TESTING:
            return '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
        else:
            return settings.G_RECAPTCHA_SITEKEY

    def __getRecaptchaSecretKey(self):
        # If we are in testing mode, use the google test sitekey:
        # https://developers.google.com/recaptcha/docs/faq
        # G_TESTING is normally False, but set to True in tests.py
        if settings.G_TESTING:
            return '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
        else:
            return settings.G_RECAPTCHA_SECRETKEY

    def __validateReCaptcha(self, request):

        # Get the google recaptcha
        captcha = request.POST.get('g-recaptcha-response')

        # Check if the recaptcha is valid
        url = 'https://www.google.com/recaptcha/api/siteverify'

        values = {
                'secret': self.__getRecaptchaSecretKey(),
                'response': captcha,
            }

        r = requests.post(url, data=values)
        result = r.json()

        # Return success or failure
        if result['success']:
            return True
        else:
            raise ValidationError('Invalid recaptcha!')

    def __processForm(self, request, form, context):

        if not (form.is_valid() and self.__validateReCaptcha(request)):

            # Form is invalid, but no errors were raised in
            # recaptcha etc.
            return False

        else:

            # Form is valid, get the data from the form
            sender_name = form.cleaned_data['form_name']
            sender_email = form.cleaned_data['form_email']
            subject = form.cleaned_data['form_subject']
            message = form.cleaned_data['form_message']

            # Generate the new email message
            strNewSubject = "CONTACT FROM MarksWebsite: - [ " + subject + " ]"
            strNewMessage = "Sender Name: " + sender_name + "\n" \
                            + "Sender Email: " + sender_email + "\n\n" \
                            + "Subject: " + subject + "\n\n\n" \
                            + "Message: \n\n" + message

            # Please note that your EC2 role needs access to SES for this to
            # work.

            # Create a new SES resource and specify a region.   SES is in
            # eu-west-1 NOT eu-west-2
            client = boto3.client('ses', region_name="eu-west-1")

            # Try to send the email.
            # Yahoo prevents you from sending via ses, so I am going to send
            # an email to my yahoo from my gmail account.   At some point in
            # the future, I need to adjust this once I have a proper domain,
            # but I don't have time to do that yet. Both email addresses have
            # been authorised in SES. I cannot send to external email addresses
            # unless it is adjusted by AWS and I am not prepared to do this
            # yet.   For this reason, I cannot currently respond to the sender.

            tmpDestination = {'ToAddresses':
                              ["mark_john_wilson@yahoo.co.uk", ], }
            tmpMessage = {
                    'Body': {
                        'Text': {
                            'Charset': "UTF-8",
                            'Data': strNewMessage,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': strNewSubject,
                    },
                }
            # Provide the contents of the email.
            response = client.send_email(
                Destination=tmpDestination,
                Message=tmpMessage,
                Source="mark.john.wilson@gmail.com"
            )

            # Email sent and no error's
            return True

    def get(self, request, **kwargs):

        # Form initially called by get, so setup default context then
        # render the form
        logger.debug('Logging debug message')
        form = ContactForm()
        context = {
                'form': form,
                'RECAPTCHA_SITEKEY': self.__getRecaptchaSiteKey(),
                'EXTRA_ERROR': '',
        }
        return render(request, 'contact.html', context=context)

    def post(self, request, **kwargs):

        # Generate and validate the form
        logger.debug('Logging debug message')
        form = ContactForm(request.POST)

        # Build a default context using the form and recaptcha keys.   Allow
        # room for an extra error
        context = {
                'form': form,
                'RECAPTCHA_SITEKEY': self.__getRecaptchaSiteKey(),
                'EXTRA_ERROR': '',
        }

        try:

            if self.__processForm(request, form, context):
                # Email sent successfully
                return render(request, 'success.html', context=None)
            else:
                # Form was invalid, so just post it without changing context
                return render(request, 'contact.html', context=context)

        except Exception as Ex:
            strReport = Ex.args[0]
            # Form is invalid
            logger.debug('ContactView - %s' % (strReport,))
            context['EXTRA_ERROR'] = strReport
            return render(request, 'contact.html', context=context)
