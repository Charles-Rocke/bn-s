from django import forms

class UserNameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,widget= forms.TextInput(attrs={'id':'signup-value'}))