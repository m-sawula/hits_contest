from django import forms


# 13:10 sobota
class AuthorForm(forms.Form):
    first_name = forms.CharField(label="First name", required=False)
    last_name = forms.CharField(label="Last name", required=False)
    band_name = forms.CharField(label="Band name")
    birth_date = forms.DateField(
        label="Birth date",
        required=False,
        widget=forms.SelectDateWidget
    )
    debut = forms.DateField(
        label="Debut date",
        required=False,
        widget=forms.SelectDateWidget
    )