from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput, FileInput, Textarea
from .models import ProgressibilityUserProfile

# Adding email, first name and last name fields to the built-in
# UserCreationForm. The below form will be used by the user to register
# with Progressibility.
class ProgressibilityUserCreationForm(UserCreationForm):
	username = forms.CharField(widget=TextInput(attrs={
			"class": "form-input",
			"placeholder": "Username",
		}), label='')
	email = forms.EmailField(required=True, widget=TextInput(attrs={
			"class": "form-input",
			"placeholder": "Email",
		}), label='')
	first_name = forms.CharField(required=True, widget=TextInput(attrs={
			"class": "form-input",
			"placeholder": "First Name",
		}), label='')
	last_name = forms.CharField(required=True, widget=TextInput(attrs={
			"class": "form-input",
			"placeholder": "Last Name",
		}), label='')
	password1 = forms.CharField(widget=PasswordInput(attrs={
			"class": "form-input",
			"placeholder": "Password",
		}), label='')
	password2 = forms.CharField(widget=PasswordInput(attrs={
			"class": "form-input",
			"placeholder": "Confirm Password",
		}), label='')

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(ProgressibilityUserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']

		if commit:
			user.save()
		return user

class ProgressibilityUserAvatarUpdateForm(forms.ModelForm):

	avatar = forms.ImageField(required=True, widget=FileInput(attrs={
			"class": "form-input",
		}), label="Select Avatar")

	class Meta:
		model = ProgressibilityUserProfile
		fields = ['avatar']

	def save(self, commit=True):
		profile = super(ProgressibilityUserAvatarUpdateForm, self).save(commit=False)
		profile.avatar = self.cleaned_data['avatar']

		if commit:
			profile.save()

		return profile

class ProgressibilityUserBioUpdateForm(forms.ModelForm):

	bio = forms.CharField(required=True, widget=Textarea(attrs={
			"class": "form-input",
		}), label="Bio")

	class Meta:
		model = ProgressibilityUserProfile
		fields = ['bio']

	def save(self, commit=True):
		profile = super(ProgressibilityUserBioUpdateForm, self).save(commit=False)
		profile.bio = self.cleaned_data['bio']

		if commit:
			profile.save()

		return profile
class ProgressibilityUserAuthenticationForm(AuthenticationForm):
	username = forms.CharField(widget=TextInput(attrs={
			"class": "form-input",
			"placeholder": "Username",
		}), label='')
	password = forms.CharField(widget=PasswordInput(attrs={
			"class": "form-input",
			"placeholder": "Password",
		}), label='')

	class Meta:
		model = User
		fields = ("username", "password")
