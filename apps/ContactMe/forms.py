from django import forms


class ContactForm(forms.Form):
    form_name = forms.CharField(widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Name *',
                                'required': 'required',
                                'minlength': '1',
                                'maxlength': '100',
                                'title': 'A Name betwee 1 and 100 characters'
                                         ' is required.'
                                }),)
    form_email = forms.CharField(widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Email *',
                                'required': 'required',
                                'minlength': '3',
                                'maxlength': '100',
                                'title': 'An Email Address between 3 and 100'
                                         ' characters is required.'
                                }),)
    form_subject = forms.CharField(widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Subject *',
                                'required': 'required',
                                'minlength': '1',
                                'maxlength': '100',
                                'title': 'A Subject between 1 less than 100'
                                         ' characters is required.'
                                }),)
    form_message = forms.CharField(widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'placeholder': 'Message *',
                                'required': 'required',
                                'minlength': '1',
                                'maxlength': '2000',
                                'title': 'A message between 1 and 2000'
                                         ' characters is required.'
                                }),)
