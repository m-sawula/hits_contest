from django import forms

class AuthorForm(forms.Form):
    first_nam = forms.CharField(label="First name", required=False)
    last_name = forms.CharField(label="Last name", required=False)
    birth_nade = forms.DateField(label="Birth date", required=False)
    band_name = forms.CharField(label="Band name")
    debut = forms.DateField(required=True)

