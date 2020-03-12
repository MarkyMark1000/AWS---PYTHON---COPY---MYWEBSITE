from django.shortcuts import render
from django.views import View
from apps.ContactMe.forms import ContactForm
import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import SuspiciousOperation

import logging
logger = logging.getLogger('ebdjango')


# Create your views here.

class ContactView(View):
    def get(self, request, **kwargs):
        logger.debug('Logging debug message')
        form = ContactForm()
        return render(request, 'contact.html', context={'form': form})

    def post(self, request, **kwargs):
        # Generate and validate the form
        logger.debug('Logging debug message')
        form = ContactForm(request.POST)
        if form.is_valid():

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

            try:

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
            # Display an error if something goes wrong.
            except Exception as Ex:
                strRet = Ex.args[0]
                logger.error(strRet)
                # Send to error templates - 400
                raise SuspiciousOperation("Error with ContactMe - " + strRet)
            else:
                logger.debug('ContactView post success')
                return render(request, 'success.html', context=None)

        else:
            # Form is invalid, show error
            logger.debug('ContactView - invalid form')
            return render(request, 'contact.html', context={'form': form})
