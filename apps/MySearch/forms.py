from django import forms


class SearchForm(forms.Form):
    form_searchText = forms.CharField(widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Search *',
                                'minlength': '1',
                                'maxlength': '30',
                                'autocomplete': 'off',
                                'title': 'A string between 1 and 30 '
                                         'characters is required.'
                                }),)
