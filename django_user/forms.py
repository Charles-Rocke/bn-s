from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class UserCreateForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields.pop('password1')
		self.fields.pop('password2')
		
	class Meta:
		model = User
		fields = ('username',)
	
	
	def save(self, commit=True):
			if not commit:
					raise NotImplementedError("Can't create User and UserProfile without database save")
			user = super(UserCreateForm, self).save(commit=True)
			user_profile = User(user=user)
			user_profile.save()
			return user, user_profile


class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.fields.pop('password')

	class Meta:
		model = User
		fields = ('username',)
		
	username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))